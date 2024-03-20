import os, json
from ui import ArrowMenu, clean_on_exit, get_open_file_name, get_input_name_decorated, mw, add_border, ArrowMenuDecorated, Window, navigate_controller, TextArea, splash_decorated
from monsters import generate_monster_pack
from enums import *
from character import Character
from party import Party, is_dead_party
from bisect import insort
from createchar import create_or_edit_char
from monsters import Monster
from editparty import party_details


def character_quick_ref(c):
    return '{}, {} {} {}'.format(c._name, Gender(c._gender).name, Race(c._race).name, Class(c._class).name) if c else 'None'
        

def load_character(file):
    filename = 'chars/' + file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return Character.deserialize(data)


def pick_character(c):
    bk = c
    options = ['Create', 'Load', 'Edit', 'Remove' ,'', 'Done', 'Back']
    rc = character_quick_ref(c) if c else ['[Empty slot]']
    with ArrowMenu(mw(), 20, 5, options, rc, min_w=50) as menu:
        while(True):
            id, fwd = menu.select()
            if id == 0:
                ch = create_or_edit_char(None)
                if ch:
                    c = ch
            elif id == 1:
                f = get_open_file_name(mw(), 3, 7, 'Pick a character', 'chars', '.chr')
                if f:
                    c = load_character(f)
            elif id == 2:
                ch = create_or_edit_char(c)
                if ch:
                    c = ch
            elif id == 3:
                c = None
            elif id == 5:
                return c
            elif id == 6:
                return bk
            menu.set_title(character_quick_ref(c) if c else '[Empty slot]')


def edit_party():
    characters = [None] * 4
    options = ['Member {}: {}'.format(i + 1, character_quick_ref(c)) for i, c in enumerate(characters)]
    options.append('')
    options.append('Done')
    options.append('Back')
    with ArrowMenu(mw(), 20, 5, options, 'Form a party', min_w=50) as menu:
        while(True):
            id, fwd = menu.select()
            if id < 4:
                characters[id] = pick_character(characters[id])
                menu.set_item(id, 'Member {}: {}'.format(id + 1, character_quick_ref(characters[id])))
            elif id == 5 and any(characters):
                return Party(characters)
            elif id == 6:
                return None


class ExtEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def save_party(name, party):
    try:
        os.mkdir('parties')
    except:
        pass
    filename = 'parties/' + name + '.par'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(party, f, cls=ExtEncoder, ensure_ascii=False, indent=4)
    return True


def load_party(file):
    filename = 'parties/' + file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return Party.deserialize(data)
    

def is_active(p):
    return p._hp > 0


class Queue:
    def __init__(self, party, monsters):
        self._len = 10
        self._time = 0
        self._participants = [(p, interval(p._attributes[Attribute.Speed])) for p in party._characters + monsters if p and is_active(p)]
        self._participants.sort(key=lambda p: p[1])

        self._timeline = []
        self._fill_timeline()

    def _fill_timeline(self):
        while len(self._timeline) < self._len:
            p = self._participants.pop(0)
            self._timeline.append(p)
            new_p = (p[0], p[1] + interval(p[0]._attributes[Attribute.Speed]))
            insort(self._participants, new_p, key=lambda p: p[1])

    def _rearrange(self):
        pass

    def deactivate(self, p):
        self._timeline = [e for e in self._timeline if e[0] != p]
        #while 

    def activate(self, p):
        pass
        
    def forward(self):
        self._timeline.pop(0)
        self._fill_timeline()

    def current(self):
        return self._timeline[0][0]
    
    def time(self):
        return self._timeline[0][1]
    

def represent_queue(queue):
    names = [t[0]._name for t in queue._timeline]
    return ' -> '.join(names)


def perform_attack(atacker, atacked):
    # TBD
    atacked._hp -= 10
    return '{} attacked {} dealing {} damage'.format(atacker._name, 'TBD', 'TBD')


def foe_attack(foe: Monster, chars):
    # TODO: select target using _targets
    # TODO: calculate attack
    return '{} attacked {} dealing {} damage'.format(foe._name, 'TBD', 'TBD')


def real_target_indexes(targets, rivals):
    result = set()
    for t in targets:
        unactives = 0
        for i in range(4):
            if rivals[i] is None or not rivals[i].is_active():
                unactives += 1
            else:
                if i >= t and i - unactives <= t:
                    result.add(i)
    return list(result)


def represent_combaters(party, foes, active):
    def party_member_repr(m):
        return [m._name, 'HP: {}/{}'.format(m._hp, m._hp_max), 'MP: {}/{}'.format(m._mp, m._mp_max)] + [e._name for e in m._effects] if m else []
    
    def foe_repr(m):
        return [m._name, 'HP: {}/{}'.format(m._hp, m._hp_max)] + [e._name for e in m._effects] if m else []
    
    result = []
    combaters = [m for m in party[::-1]] + [m for m in foes]
    activeid = combaters.index(active)
    result.append('\t\t' * activeid + '  #')
    reprs = [party_member_repr(m) for m in party[::-1]] + [foe_repr(m) for m in foes]
    count = len(max(reprs, key=lambda r: len(r)))
    for i in range(count):
        ln = ''
        for r in reprs:
            ln += r[i] if i < len(r) else ''
            ln += '\t\t'
        result.append(ln)
    return '\n'.join(result)


def combat(party: Party, foes):
    def init_wnd():
        add_border(wnd, 1, 2, 78, 18)
        add_border(wnd, 0, 0, 80, 3)
        add_border(wnd, 0, 19, 80, 6)

    def ally_repr(m: Character, w: Window):
        w.clear()
        if m is None:
            return
        w.print_at(0, 2, m._name)
        w.print_at(0, 3, 'HP:{}/{}'.format(m._hp, m._hp_max))
        w.print_at(0, 3, 'MP:{}/{}'.format(m._mp, m._mp_max))
        # TODO: effects
        if queue.current() == m:
            w.print_at(7, 0, '@')
        w.show()
    
    def foe_repr(m: Character, w: Window):
        w.clear()
        if m is None:
            return
        w.print_at(0, 2, m._name)
        w.print_at(0, 3, 'HP:{}/{}'.format(m._hp, m._hp_max))
        # TODO: effects
        if queue.current() == m:
            w.print_at(7, 0, '@')
        w.show()

    def update_wnd():
        qwnd.print_at(0, 0, represent_queue(queue), flush=True)
        for i in range (4):
            ally_repr(party._characters[i], combaters_windows[3 - i])
            foe_repr(foes[i], combaters_windows[4 + i])
        log.show()

    queue = Queue(party, foes)
    with mw().create_child(0, 0, 80, 25) as wnd:
        qwnd = wnd.create_child(1, 1, 78, 1)
        log = TextArea(wnd, 1, 20, 78, 4)
        combaters_windows = [wnd.create_child((2 + 16 * i) if i < 4 else (-49 + 16 * i), 11 if i < 4 else 3, 15, 8) for i in range(8)]
        init_wnd()
        update_wnd()
        wnd.show()
        while True:
            if queue.current() in party._characters:
                with ArrowMenuDecorated(wnd, 0, 3, ['Attack', 'Cast', 'Defend', 'Move', 'Inventory', 'Flee']) as menu:
                    id, fwd = menu.select()
                    if id == 5:
                        # TODO: check condition
                        return
                    if id == 0:
                        targets = real_target_indexes(queue.current().attack_targets(), foes)
                        if len(targets) == 0:
                            continue
                        tid, _ = navigate_controller(lambda i, j: combaters_windows[targets[i] + 4].print_at(7, 1, ' ', flush=True), 
                                            lambda i, j: combaters_windows[targets[i] + 4].print_at(7, 1, '+', flush=True), 
                                            len(targets))
                        if tid is None:
                            continue
                        target = targets[tid]
                        logln = perform_attack(queue.current(), foes[target])
                        splash_decorated(wnd, 20, 10, 40, logln, bold=True)
                        log.add(logln)
            else:
                logln = foe_attack(queue.current(), party._characters)
                splash_decorated(wnd, 20, 10, 40, logln, bold=True)
                log.add(logln)
            queue.forward()
            update_wnd()
            


def pick_event(party, area):
    # TODO events other than combat

    foes = generate_monster_pack(area)
    combat(party, foes)


def party_actions(party):
    options = ['Rest', 'Rearrange']
    with ArrowMenuDecorated(mw(), 37, 8, options) as menu:
        id, fwd = menu.select()
        if not fwd:
            return


def main_loop(name, party):
    area = 'Arena'

    options = ['Forward!', 'Party actions', 'Character details', 'Save & exit']
    with ArrowMenuDecorated(mw(), 20, 5, options, 'Main loop') as menu:
        while(True):
            id, fwd = menu.select()
            if not fwd:
                return
            if id == 0:
                pick_event(party, area)
                if is_dead_party(party):
                    return
            elif id == 1:
                party_actions(party)
            elif id == 2:
                party_details(party)
            elif id == 3:
                if save_party(name, party):
                    return


def main_menu():
    os.system('cls')
    with ArrowMenuDecorated(mw(), 20, 5, ['New party', 'Continue', 'Exit'], 'Main menu') as menu:
        while(True):
            id, fwd = menu.select()
            if not fwd:
                return
            if id == 2:
                clean_on_exit()
                return
            elif id == 0:
                name = get_input_name_decorated(mw(), 20, 12, 40, 'Enter party name: ')
                if not name:
                    continue
                party = edit_party()
                if not party:
                    continue
                if save_party(name, party):
                    main_loop(name, party)
            elif id == 1:
                f = get_open_file_name(mw(), 10, 2, 'Pick a party ', 'parties', '.par')
                if f:
                    party = load_party(f)
                    main_loop(f[:-4], party)

main_menu()
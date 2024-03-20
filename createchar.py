import json, copy, os
from enums import *
from ui import ArrowMenu, ArrowMenuDecorated, get_input_name_decorated, mw, add_border, add_window_border, Window
from character import Character, calculate_bases, race_talants
from forms import init_character_panel, update_character_panel


def serialize_character(c):
    try:
        os.mkdir('chars')
    except:
        pass
    filename = 'chars/' + c._name + '.chr'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(c.__dict__, f, ensure_ascii=False, indent=4)


def input_name(c: Character, wnd: Window):
    name = get_input_name_decorated(wnd, 10, 2, 21, 'Name: ', c._name, bold=True)
    c._name = name
    return name != ''


def input_gender(c: Character, wnd: Window):
    with ArrowMenuDecorated(wnd, 20, 3, [Gender(i).name for i in range(len(Gender))], '', int(c._gender) if c._gender else 0, bold=True) as menu:
        id, fwd = menu.select()
        if not fwd:
            c._gender = None
            return False
        else:
            c._gender = id
            # TODO: update attrs
            return True
            

def input_age(c: Character, wnd: Window):
    while (True):
        age_s = get_input_name_decorated(wnd, 10, 4, 11, 'Age: ', str(c._age) if c._age else '', '0-9', bold=True)
        if not age_s:
            return False
        try:
            age = int(age_s)
        except:
            continue
        if (age < 20 or age > 50):
            continue
        c._age = age
        return True
    

def input_race(c: Character, wnd: Window):
    with ArrowMenuDecorated(wnd, 20, 5, [Race(i).name for i in range(len(Race))], '', int(c._race) if c._race else 0, bold=True) as menu:
        while True:
            id, fwd = menu.select()
            if not fwd:
                c._race = None
                return False
            else:
                if id == Race.Sirena and c._gender == Gender.Male:
                    # TODO: explain that its impossible
                    continue
                c._race = id
                return True
            

def input_talant(c: Character, wnd: Window):
    talants = race_talants[int(c._race)]
    with ArrowMenuDecorated(wnd, 20, 6, [t.name for t in talants], '', 0, bold=True) as menu:
        id, fwd = menu.select()
        if not fwd:
            c._talant = None
            return False
        else:
            c._talant = talants[id]
            # TODO: update attrs
            return True
            

def input_class(c: Character, wnd: Window):
    with ArrowMenuDecorated(wnd, 20, 7, [Class(i).name for i in range(len(Class))], '', int(c._class) if c._class else 0, bold=True) as menu:
        id, fwd = menu.select()
        if not fwd:
            c._class = None
            return False
        else:
            c._class = id
            # TODO: update attrs
            return True


def input_base_attrs(c: Character, wnd: Window):
    def update():
        w.print_at(18, 1, ' ' + str(points), align_right=True)
        for i in range(len(Attribute)):
            w.print_at(18, i + 3, ' ' + str(c._attributes[i] + c._attrbonuses[i]), align_right=True)
        w.show()

    points = 5
    c._attrbonuses = [0] * len(Attribute)
    calculate_bases(c)

    with wnd.create_child(10, 9, 21, 13) as w:
        add_window_border(w, True)
        update()
        w.show()
        with ArrowMenu(w, 1, 1, [Attribute(i).name for i in range(len(Attribute))] + ['', 'Done', 'Back'], 'Points left:') as menu:
            while(True):
                id, fwd = menu.select()
                if id == 8:
                    c._attrbonuses = [0] * len(Attribute)
                    return False
                if id == 7:
                    return True
                else:
                    if fwd:
                        if c._attributes[id] + c._attrbonuses[id] == 10:
                            continue
                        required_points = 1 if c._attrbonuses[id] < 0 else c._attrbonuses[id] + 1
                        if (required_points > points):
                            continue
                        c._attrbonuses[id] += 1
                        points -= required_points
                    else:
                        if c._attributes[id] + c._attrbonuses[id] == 1 or c._attrbonuses[id] <= -2:
                            continue
                        gained_points = 1 if c._attrbonuses[id] <= 0 else c._attrbonuses[id]
                        c._attrbonuses[id] -= 1
                        points += gained_points
                    update()


def confirm(c, wnd):
    with ArrowMenuDecorated(wnd, 56, 17, ['Yes', 'No'], ' All correct?', bold=True) as menu:
        id, fwd = menu.select()
        return id == 0


def create_or_edit_char(ch: Character):
    def init_wnd():
        add_border(wnd, 10, 2, 70, 23)
        add_border(wnd, 10, 0, 15, 3)
        add_border(wnd, 0, 2, 11, 3)
        wnd.print_at(11, 2, '             ')
        wnd.print_at(2, 3, 'Attrs    ')
        init_character_panel(panel)
        

    def update_wnd():
        wnd.print_at(11, 1, 'New character' if not c._name else '             ')
        wnd.print_at(11, 1, c._name)
        update_character_panel(panel, c)
        

    c = copy.deepcopy(ch) if ch else Character()
    with mw().create_child(0, 0, 80, 25) as wnd:
        panel = wnd.create_child(11, 3, 68, 21)
        init_wnd()
        update_wnd()
        wnd.show()

        steps = [input_name, input_gender, input_age, input_race, input_talant, input_class, input_base_attrs, confirm]
        index = 0 if not ch else len(steps) - 1
        while index < len(steps):
            advance = steps[index](c, wnd)
            calculate_bases(c)
            update_wnd()
            wnd.show()
            if advance:
                index += 1
            else:
                index -= 1
                if index < 0:
                    return None
        calculate_bases(c)
        serialize_character(c)
        return c

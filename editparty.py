from enums import *
from ui import mw, add_border, navigate_controller, Window
from party import Party
from character import Character
from forms import init_character_panel, update_character_panel


def init_inventory_panel(panel: Window):
    panel.print_at(1, 0, 'Equiped')
    for i in range(int(len(EquipSlot))):
        panel.print_at(1, 2 + i, EquipSlot(i).name)
    panel.print_at(1, 15, 'Equip Weight:')
    panel.print_at(1, 16, 'Armor:')

    panel.print_at(1, 17, 'Brew:')

    panel.print_at(40, 0, 'Inventory')


def update_inventory_panel(panel: Window, c: Character):
    pass
    

def party_details(p: Party):
    def init_wnd():
        add_border(wnd, 10, 2, 70, 23)
        for i in range(4):
            add_border(wnd, 10 + i * 17, 0, 18, 3)
            wnd.print_at(12 + i * 17, 1, p._characters[i]._name if p._characters[i] is not None else '')
        add_border(wnd, 0, 2, 11, 7)
        wnd.print_at(2, 3, 'Attrs ')
        wnd.print_at(0, 4, '+---------+')
        wnd.print_at(2, 5, 'Invent')
        wnd.print_at(0, 6, '+---------+')
        wnd.print_at(2, 7, 'Spells')

        add_border(wnd, 0, 22, 11, 3)
        wnd.print_at(2, 23, 'Exit')
        

    def update_wnd():
        pass

    def controller_exit(ci, ti):
        wnd.print_at(11 + ci * 17, 2, '----------------', flush=True)
        wnd.print_at(10, 3 + ti * 2 if ti != 3 else 23, '|', flush=True)

    def controller_enter(ci, ti):
        wnd.print_at(11 + ci * 17, 2, '                ', flush=True)
        wnd.print_at(10, 3 + ti * 2 if ti != 3 else 23, ' ', flush=True)

        panel.clear()
        c = p._characters[ci]
        if c is not None:
            if ti == 0:
                init_character_panel(panel)
                update_character_panel(panel, c)
            elif ti == 1:
                init_inventory_panel(panel)
                update_inventory_panel(panel, c)
        panel.show()


    with mw().create_child(0, 0, 80, 25) as wnd:
        panel = wnd.create_child(11, 3, 68, 21)
        init_wnd()
        update_wnd()
        wnd.show()
        while True:
            ch, tab = navigate_controller(controller_exit, controller_enter, 4, 4, 0, 0)
            if ch is None or tab == 3:
                return

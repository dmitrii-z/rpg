from enums import *
from character import Character
from ui import add_v_line, Window


def init_character_panel(panel: Window):
    add_v_line(panel, 19)
    add_v_line(panel, 39)

    panel.print_at(1, 0, 'Name:')
    panel.print_at(1, 1, 'Gender:')
    panel.print_at(1, 2, 'Age:')
    panel.print_at(1, 3, 'Race:')
    panel.print_at(1, 4, 'Talant:')
    panel.print_at(1, 5, 'Class:')
    
    for i in range(int(len(Attribute))):
        panel.print_at(1, 7 + i, Attribute(i).name)

    panel.print_at(1, 14, 'Resists:')
    for i in range(int(len(Resist))):
        panel.print_at(1, 15 + i, Resist(i).name)

    panel.print_at(41, 0, 'Level:')
    panel.print_at(41, 1, 'XP:')
    panel.print_at(41, 2, 'XP to lvlup:')
    panel.print_at(41, 4, 'HP:')
    panel.print_at(41, 5, 'MP:')
    panel.print_at(41, 6, 'Equip:')
    panel.print_at(41, 7, 'Armor:')


def update_character_panel(panel: Window, c: Character):
    panel.print_at(17, 0, c._name, align_right=True)
    panel.print_at(17, 1, Gender(c._gender).name if c._gender is not None else '', align_right=True)
    panel.print_at(17, 2, str(c._age), align_right=True)
    panel.print_at(17, 3, Race(c._race).name if c._race is not None else '', align_right=True)
    panel.print_at(17, 4, Skill(c._talant).name if c._talant is not None else '', align_right=True)
    panel.print_at(17, 5, Class(c._class).name if c._class is not None else '', align_right=True)

    for i in range(int(len(Attribute))):
        panel.print_at(17, 7 + i, str(c._attributes[i]), align_right=True)
        
    for i in range(int(len(Resist))):
        panel.print_at(17, 15 + i, str(c._resists[i]) + '%', align_right=True)

    j = 0
    for i in range(len(c._skill_potencials)):
        if c._skill_potencials[i] > 0:
            panel.print_at(21, j, Skill(i).name)
            panel.print_at(33, j, str(c._skills[i]), align_right=True)
            panel.print_at(35, j, '+' * c._skill_potencials[i])
            j += 1

    panel.print_at(66, 0, str(c._level), align_right=True)
    panel.print_at(66, 1, str(c._exp), align_right=True)
    panel.print_at(66, 2, '---', align_right=True)
    panel.print_at(66, 4, '{}/{}'.format(c._hp, c._hp_max), align_right=True)
    panel.print_at(66, 5, '{}/{}'.format(c._mp, c._mp_max), align_right=True)
    panel.print_at(66, 6, str(c._max_equip_weight), align_right=True)

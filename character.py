import copy
from enums import *


class Character:
    def __init__(self):
        self._name = ''

        self._attributes = [5] * len(Attribute)
        self._attrbonuses = [0] * len(Attribute)
        self._gender = None
        self._age = 0
        self._race = None
        self._talant = None
        self._class = None

        self._hp_max = 0
        self._mp_max = 0
        self._max_equip_weight = 0
        self._hp = 0
        self._mp = 0
        self._exp = 0
        self._level = 1
        self._resists = [0] * len(Resist)
        self._effects = []
        self._equip = [None] * len(EquipSlot)

        self._skill_potencials = [0] * len(Skill)
        self._skills = [0] * len(Skill)
        # spells...

    @staticmethod
    def deserialize(data):
        c = Character()
        c.__dict__ = copy.copy(data)
        return c
    
    def is_active(self):
        return self._hp > 0 and not any(e.makes_inactive() for e in self._effects)
    
    def attack_targets(self):
        # TBD
        return (0, 1)


def calculate_bases(c: Character):
    c._attributes = [5] * len(Attribute)
    if c._gender is not None:
        c._attributes[Attribute.Strength if c._gender == Gender.Male else Attribute.Willpower] += 1
    if c._age:
        if c._age < 30:
            c._attributes[Attribute.Agility] += 1
        if c._age < 40:
            c._attributes[Attribute.Toughness] += 1
        else:
            c._attributes[Attribute.Intellect] += 1
    race_attr = (
        (1, 0, 0, 1, 0, 0),     # human
        (-1, 0, -1, 1, 3, 0),   # eldar
        (-1, 3, -1, 0, 0, 1),   # woodelf
        (0, 1, -1, 1, 1, 0),    # darkelf
        (1, -2, 2, 1, 1, -1),   # dwarf
        (-2, 2, -2, 2, 2, 0),   # gnome
        (-2, 3, -2, 2, 0, 1),   # pixie
        (0, 0, 0, 2, 0, 0),     # tiefling
        (4, -2, 4, 0, -2, -2),  # troll
        (2, 0, 2, -1, -1, 0),   # orc
        (0, 2, -1, -1, -1, 3),  # goblin
        (-1, 1, -1, 1, 1, 1),   # gremlin
        (1, 1, 0, 0, -1, 1),    # tifon
        (0, 1, 0, 2, -1, 0)     # sirena
    )
    if c._race is not None:
        for i in range(len(Attribute)):
            c._attributes[i] += race_attr[int(c._race)][i]
    if hasattr(c, '_attrbonuses'):  # TODO: could be removed when all saved chars has it
        for i in range(len(Attribute)):
            c._attributes[i] += c._attrbonuses[i]

    hp_for_level = (5, 4, 3, 3, 2, 2, 2, 1, 3, 3, 2, 2, 3, 3) # class dependent
    mp_for_level = (0, 0, 2, 2, 3, 3, 3, 4, 2, 1, 2, 2, 1, 0) # class dependent

    c._hp_max = c._level * (hp_for_level[c._class] if c._class is not None else 0) + c._attributes[Attribute.Toughness] * HpForToughness
    c._mp_max = c._level * (mp_for_level[c._class] if c._class is not None else 0) + c._attributes[Attribute.Intellect] * ManaForIntellect
    c._hp = c._hp_max
    c._mp = c._mp_max
    c._max_equip_weight = c._attributes[Attribute.Strength] * EquipWeightForStrength
    
    class_skill_potencials = (
        # Polearm Sword Hammer Axe Knife Staff Hand Bow Firearm Leather Chain Plate Shield Fire Cold Air Light Dark Meditation Atletic Craft Alchemy Singing Sense 
         (2,      0,    2,     3,  1,    0,    2,   1,  0,      3,      2,    0,    1,     0,   0,   0,  0,    0,   0,         3,      0,    0,      1,      1),  # Barbarian
         (3,      3,    2,     1,  1,    1,    1,   2,  0,      1,      2,    3,    3,     0,   0,   0,  0,    0,   0,         2,      1,    0,      0,      0),  # Knight
         (1,      2,    3,     0,  0,    1,    0,   0,  0,      2,      2,    2,    1,     0,   0,   0,  2,    0,   1,         1,      0,    1,      1,      1),  # Paladin
         (0,      0,    0,     0,  0,    3,    2,   0,  0,      2,      0,    0,    0,     0,   0,   0,  2,    2,   3,         1,      0,    0,      1,      1),  # Monk
         (0,      0,    0,     0,  2,    0,    3,   0,  0,      2,      0,    0,    0,     0,   0,   0,  0,    2,   1,         1,      0,    0,      0,      2),  # Spy
         (0,      0,    0,     0,  2,    2,    0,   1,  0,      2,      1,    0,    0,     0,   0,   0,  3,    3,   3,         0,      0,    1,      2,      1),  # Cleeric
         (0,      0,    1,     0,  1,    2,    1,   0,  0,      2,      0,    0,    0,     2,   2,   2,  2,    2,   2,         0,      0,    0,      2,      1),  # Shaman
         (0,      0,    0,     0,  1,    2,    0,   0,  0,      2,      0,    0,    0,     3,   3,   3,  0,    0,   3,         0,      0,    2,      0,      0),  # Wizard
         (0,      2,    1,     0,  0,    2,    0,   1,  0,      2,      2,    0,    1,     2,   2,   2,  0,    0,   2,         1,      1,    0,      0,      0),  # Spellblade
         (1,      1,    0,     1,  3,    1,    2,   3,  1,      2,      1,    0,    0,     1,   1,   1,  0,    0,   0,         0,      2,    1,      0,      3),  # Scout
         (0,      0,    0,     0,  2,    1,    0,   0,  1,      2,      0,    0,    0,     2,   2,   2,  0,    0,   1,         0,      1,    3,      0,      0),  # Alchemist
         (0,      0,    0,     0,  2,    0,    2,   1,  0,      2,      1,    0,    0,     0,   0,   0,  1,    1,   0,         1,      1,    0,      3,      2),  # Bard
         (0,      0,    3,     1,  0,    0,    2,   0,  2,      1,      2,    1,    0,     1,   0,   0,  0,    0,   0,         2,      3,    2,      0,      0),  # Blacksmith
         (0,      1,    0,     0,  2,    0,    1,   2,  3,      1,      3,    0,    1,     0,   0,   0,  0,    0,   0,         1,      2,    2,      0,      1)   # Musketeer
    )

    c._skill_potencials = [0] * len(Skill)
    c._skills = [0] * len(Skill)
    if c._class is not None:
        for i, p in enumerate(class_skill_potencials[c._class]):
            c._skill_potencials[i] = p
            if p == 3:
                c._skills[i] = 5
    if c._talant:
        c._skill_potencials[c._talant] += 1
        c._skills[c._talant] += 5

    race_resists = (
       # Phisic Fire Cold Air Light Dark
        (0,     0,   0,   0,  20,   20),  # Human
        (-10,   0,   0,   0,  0,    50),  # Eldar
        (0,     10,  10,  20, 0,    0),   # WoodElf
        (0,     10,  0,   0,  -10,  30),  # DarkElf
        (10,    20,  20,  10, 0,    0),   # Dwarf
        (0,     20,  20,  20, 0,    0),   # Gnome
        (-10,   10,  10,  10, 10,   10),  # Pixie
        (0,     50,  0,   0,  -20,  10),  # Tiefling
        (30,    20,  10,  0,  -40,  0),   # Troll
        (10,    10,  0,   0,  -20,  10),  # Orc
        (-10,   0,   0,   0,  -20,  20),  # Goblin
        (0,     10,  0,   30, 0,    0),   # Gremlin
        (10,    0,   30,  0,  0,    -10), # Typhon
        (0,     0,   50,  0,  0,    0)    # Sirena
    )

    c._resists = [0] * len(Resist)
    if c._race is not None:
        for  i, r in enumerate(race_resists[c._race]):
            c._resists[i] = r


race_talants = (
    (Skill.Craft, Skill.Light, Skill.Firearm, Skill.Alchemy),
    (Skill.Air, Skill.Cold, Skill.Fire, Skill.Meditation),
    (Skill.Sword, Skill.Knife, Skill.Bow, Skill.Singing),
    (Skill.Dark, Skill.Sense, Skill.Meditation),
    (Skill.Hammer, Skill.Shield, Skill.Craft, Skill.Plate),
    (Skill.Air, Skill.Sense, Skill.Alchemy),
    (Skill.Knife, Skill.Sense, Skill.Singing),
    (Skill.Fire, Skill.Alchemy, Skill.Bow),
    (Skill.Hammer, Skill.Hand, Skill.Atletic),
    (Skill.Axe, Skill.Atletic, Skill.Chain),
    (Skill.Knife, Skill.Bow, Skill.Sense),
    (Skill.Craft, Skill.Alchemy, Skill.Firearm),
    (Skill.Polearm, Skill.Firearm, Skill.Leather),
    (Skill.Dark, Skill.Cold, Skill.Singing)
)
import random
from enums import *


MonsterHpForClass = 3


class Monster:
    def __init__(self):
        self._name = ''
        self._spice = ''
        self._attributes = [5] * len(Attribute)
        self._level = 1
        self._hp_max = 0
        self._hp = 0
        
        self._resists = [0] * len(Resist)
        self._targets = (0, 0)
        self._special_attacks = []
        self._effects = []

    def __repr__(self):
        return self._name
    
    def is_active(self):
        return self._hp > 0 and not any(e.makes_inactive() for e in self._effects)


monster_templates = {
    # spice         pos     attr                resist                   targets special
    'Green Slime': ((0, 3), (3, 2, 2, 0, 1, 5), (0, 0, 0, 0, -20, -20),  (0, 0), []),
    'Red Slime':   ((0, 3), (3, 2, 2, 0, 1, 5), (0, 30, 0, 0, -20, -20), (0, 0), []),
    'White Slime': ((0, 3), (3, 2, 2, 0, 1, 5), (0, 0, 0, 30, -20, -20), (0, 0), []),
    'Blue Slime':  ((0, 3), (3, 2, 2, 0, 1, 5), (0, 0, 30, 0, -20, -20), (0, 0), [])
}


def generate_monster(spice: str, name: str) -> Monster:
    templ = monster_templates[spice]
    m = Monster()
    m._name = name
    m._spice = spice
    m._attributes = [a for a in templ[1]]
    m._resists = [a for a in templ[2]]
    m._targets = templ[3]
    m._special_attacks = templ[4]
    m._hp_max = m._level * MonsterHpForClass + m._attributes[Attribute.Toughness] * HpForToughness
    m._hp = m._hp_max
    return m


monsters_in_areas = {
    'Arena': ('Green Slime', 'Red Slime', 'White Slime', 'Blue Slime'),
    'Mirkwood': (),
    'Darkmoor': (),
}


monsters_in_areas_and_positions = {}
for area, monsters in monsters_in_areas.items():
    monsters_in_positions = [[], [], [], []]
    for monster in monsters:
        position_range = monster_templates[monster][0]
        for p in range(3):
            if position_range[0] <= p <= position_range[1]:
                 monsters_in_positions[p].append(monster)
    for p in range(4):
        if not monsters_in_positions[p]:
            monsters_in_positions[p] = [monster for monster in monsters]
    monsters_in_areas_and_positions[area] = monsters_in_positions


def generate_monster_pack(area: str):
    monsters_in_positions = monsters_in_areas_and_positions[area]
    spices = [random.choice(monsters_in_positions[p]) for p in range(4)]
    indexes = [0, 0, 0, 0]
    counts = {}
    for p, spice in enumerate(spices):
        counts[spice] = counts.get(spice, 0) + 1
        indexes[p] = counts[spice]
    return [generate_monster(spices[p], '{} {}'.format(spices[p], indexes[p]) if counts[spices[p]] > 1 else spices[p]) for p in range(4)]

# pack = generate_monster_pack('Arena')
# print(pack)

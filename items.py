from enums import EquipSlot, EquipType, Rarity, Resist, Attribute, Skill
from enum import IntEnum


class ItemEffectType(IntEnum):
    Armor = 0
    HP = 1
    MP = 2
    Attribute = 3
    Element = 4
    Skill = 5


class ItemEffect:
    def __init__(self):
        self._type = None
        self._sybtype = None
        self._bonus = 0

    def __repr__(self):
        def fmt(name):
            return '{} {}{}'.format(name, '+' if self._bonus >= 0 else '', self._bonus)

        if self._type is None:
            return '<ItemEffect.None>'
        elif self._type in (ItemEffectType.Armor, ItemEffectType.HP, ItemEffectType.MP):
            return fmt(ItemEffectType(self._type).name)
        elif self._type == ItemEffectType.Attribute:
            return fmt(Attribute(self._sybtype).name)
        elif self._type == ItemEffectType.Element:
            return fmt(Resist(self._sybtype).name)
        elif self._type == ItemEffectType.Skill:
            return fmt(Skill(self._sybtype).name)


class Item:
    def __init__(self):
        self._name = ''
        self._full_name = ''
        self._price = 0
        self._weight = 0
        self._type = None
        self._bonus = 0
        self._rarity = None
        self._twoHanded = False     # weapoons only
        self._effects = []
        self._identified = False

    def armor(self):
        armor_equip = (EquipType.Leather, EquipType.Chain, EquipType.Plate, EquipType.Shield, EquipType.Headgear, EquipType.Footgear, EquipType.Gauntlets, EquipType.Cloak)
        return self._bonus if self._type is not None and self._type in armor_equip else 0
    
    def __repr__(self):
        return self._full_name if self._identified else '{} (Unidentified)'.format(self._name)
    
    def details(self):
        return [e.__repr() for e in self._effects].join(', ')

    def id_level(self):
        pass


item_templates = (
    #CL name       Pr Wt                     Bonus
    (1, 'Sandals', 5, 1, EquipType.Footgear, 1),
)
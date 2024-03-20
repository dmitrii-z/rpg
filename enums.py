from enum import IntEnum


class Gender(IntEnum):
    Male = 0
    Female = 1


class Attribute(IntEnum):
    Strength = 0
    Agility = 1
    Toughness = 2
    Willpower = 3
    Intellect = 4
    Speed = 5


HpForToughness = 5
ManaForIntellect = 5
EquipWeightForStrength = 5

def interval(speed):
    return 20 - speed


class Race(IntEnum):
    Human = 0
    Eldar = 1
    WoodElf = 2
    DarkElf = 3
    Dwarf = 4
    Gnome = 5
    Pixie = 6
    Tiefling = 7
    Troll = 8
    Orc = 9
    Goblin = 10
    Gremlin = 11
    Typhon = 12
    Sirena = 13


class Class(IntEnum):
    Barbarian = 0
    Knight = 1
    Paladin = 2
    Monk = 3
    Spy = 4
    Cleeric = 5
    Shaman = 6
    Wizard = 7
    Spellblade = 8
    Scout = 9
    Alchemist = 10
    Bard = 11
    Blacksmith = 12
    Musketeer = 13


class Skill(IntEnum):
    Polearm = 0
    Sword = 1
    Hammer = 2
    Axe = 3
    Knife = 4
    Staff = 5
    Hand = 6
    Bow = 7
    Firearm = 8
    Leather = 9
    Chain = 10
    Plate = 11
    Shield = 12
    Fire = 13
    Cold = 14
    Air = 15
    Light = 16
    Dark = 17
    Meditation = 18
    Atletic = 19
    Craft = 20
    Alchemy = 21
    Singing = 22
    Sense = 23


class Resist(IntEnum):
    Phisic = 0
    Fire = 1
    Cold = 2
    Air = 3
    Light = 4
    Dark = 5


class EquipSlot(IntEnum):
    Body = 0
    Head = 1
    Foot = 2
    Arms = 3
    RightHand = 4
    LeftHand = 5
    AltWeapoon = 6
    Cloak = 7
    Belt = 8
    Neck = 9
    Ring1 = 10
    Ring2 = 11


class EquipType(IntEnum):
    Polearm = 0
    Sword = 1
    Hammer = 2
    Axe = 3
    Knife = 4
    Staff = 5
    Hand = 6
    Bow = 7
    Firearm = 8
    Musical = 9
    Leather = 10
    Chain = 11
    Plate = 12
    Shield = 13
    Headgear = 14
    Footgear = 15
    Gauntlets = 16
    Cloak = 17
    Belt = 18
    Necklage = 19
    Ring = 20
    Potion = 21
    Scroll = 22
    Amulet = 23
    Ingredient = 24


class Rarity(IntEnum):
    Worn = 0
    Ordinary = 1
    Perfect = 2
    Uncommon = 3
    Rare = 4
    Epic = 5
    Legendary = 6
    Mythic = 7
    Exotic = 8

import copy
from character import Character


class Party:
    def __init__(self, characters):
        self._characters = characters
        self._max_inventory_weight = 0
        self._inventory = []
        self._gold = 0

    def inventory_weight(self):
        return sum(item._weight for item in self._inventory)
    
    @staticmethod
    def deserialize(data):
        p = Party([])
        p.__dict__ = copy.copy(data)
        p._characters = [Character.deserialize(c) if c else None for c in data['_characters']]
        return p


def is_dead_party(party):
    return all(c is None or c._hp <= 0 for c in party._characters)

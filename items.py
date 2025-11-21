from dataclasses import dataclass
from constants import RANDOM_SEED
import random

rng = random.Random(RANDOM_SEED)

@dataclass
class Item:
    name: str
    damage: int
    damage_chance: float
    scenery: float

    def damage_now(self, variable_chance: float = 1.0) -> int: # The damage at the given moment
        return self.damage if rng.random() <= (self.damage_chance * variable_chance) else 0

WEAPONS = [
    Item("Axe", 5, 0.95, 0.5),
    Item("Trident", 8, 0.7, 0.75),
    Item("Long Sword", 7, 0.85, 0.65),
    Item("Knife", 10, 0.45, 0.75),
    Item("Bow", 9, 0.6, 0.95),
    Item("War Hammer", 12, 0.55, 0.4),
    Item("Short Sword", 6, 0.9, 0.6),
    Item("Spear", 7, 0.8, 0.7),
    Item("Crossbow", 11, 0.5, 0.9),
    Item("Dagger", 4, 0.98, 0.8),
    Item("Mace", 9, 0.65, 0.45),
    Item("Scimitar", 8, 0.75, 0.7),
    Item("Throwing Axe", 6, 0.7, 0.85),
    Item("Halberd", 10, 0.6, 0.55),
    Item("Whip", 3, 0.9, 1.0),
]
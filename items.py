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
    Item("Bow", 6, 0.6, 0.95)
]
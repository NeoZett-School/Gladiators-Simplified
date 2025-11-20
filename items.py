from dataclasses import dataclass
from constants import RANDOM_SEED
import random

rng = random.Random(RANDOM_SEED) # We literally use this everywhere, and it is a constant.

@dataclass
class Item:
    name: str
    damage: int
    damage_chance: float
    scenery: float

    def damage_now(self, variable_chance: float = 1.0) -> int: # The damage at the given moment
        return self.damage if rng.random() <= self.damage_chance * variable_chance else 0

WEAPONS = [
    Item("Axe", 5, 0.75, 0.5),
    Item("Trident", 8, 0.25, 0.75),
]
from dataclasses import dataclass
import random

from constants import RANDOM_SEED

rng = random.Random(RANDOM_SEED)

@dataclass
class Item:
    name: str
    damage: int
    damage_chance: float

    def should_attack(self) -> int:
        return self.damage if rng.random() <= self.damage_chance else 0
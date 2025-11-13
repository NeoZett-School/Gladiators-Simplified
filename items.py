from dataclasses import dataclass
import random

rng = random.Random(42)

@dataclass
class Item:
    name: str
    damage: int
    damage_chance: float

    def attack(self) -> int:
        return self.damage if rng.random() <= self.damage_chance else 0
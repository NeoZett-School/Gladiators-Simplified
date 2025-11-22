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
    blood: int
    blood_ticks: int
    rarity: str

    def damage_now(self, variable_chance: float = 1.0) -> int:
        return self.damage if rng.random() <= (self.damage_chance * variable_chance) else 0

WEAPONS = [
    Item("Axe", 5, 0.95, 0.5, 0, 0, "common"),                  # common
    Item("Trident", 8, 0.7, 0.75, 0, 0, "uncommon"),            # uncommon
    Item("Long Sword", 7, 0.85, 0.65, 0, 0, "uncommon"),        # uncommon
    Item("Knife", 10, 0.45, 0.75, 0, 0, "rare"),                # rare
    Item("Bow", 9, 0.6, 0.95, 0, 0, "uncommon"),                # uncommon
    Item("War Hammer", 12, 0.55, 0.4, 0, 0, "rare"),            # rare
    Item("Short Sword", 6, 0.9, 0.6, 3, 1, "common"),           # common
    Item("Spear", 7, 0.8, 0.7, 3, 1, "rare"),                   # common
    Item("Crossbow", 11, 0.5, 0.9, 0, 0, "rare"),               # rare
    Item("Dagger", 4, 0.98, 0.8, 2, 2, "common"),               # common
    Item("Mace", 9, 0.65, 0.45, 3, 1, "uncommon"),              # uncommon
    Item("Scimitar", 8, 0.75, 0.7, 4, 1, "uncommon"),           # uncommon
    Item("Throwing Axe", 6, 0.7, 0.85, 0, 0, "common"),         # common
    Item("Halberd", 10, 0.6, 0.55, 0, 0, "rare"),               # rare
    Item("Whip", 3, 0.9, 1.0, 0, 0, "common"),                  # common
    Item("Escalibur", 20, 0.1, 0.95, 0, 0, "legendary"),        # legendary
    Item("Reavers Pike", 15, 0.6, 0.95, 5, 3, "legendary"),     # legendary/overpowered
    Item("Gods Finger", 100, 1.0, 1.0, 0, 0, "experimental"),   # experimental/unobtainable/overpowered
    Item("Air", 0.0, 0.0, 0.0, 0, 0, "experimental")            # experimental/unobtainable/overpowered
]

# Rarity weights matching the order above
# Higher number = more common drop
WEAPON_RARITY = [
    1.0,  # Axe
    0.6,   # Trident
    0.6,   # Long Sword
    0.3,   # Knife
    0.6,   # Bow
    0.3,   # War Hammer
    1.0,  # Short Sword
    1.0,  # Spear
    0.3,   # Crossbow
    1.0,  # Dagger
    0.6,   # Mace
    0.6,   # Scimitar
    1.0,  # Throwing Axe
    0.3,   # Halberd
    1.0,  # Whip
    0.1,   # Escalibur (legendary)
    0.05,    # Reavers Pike (legendary/strongest)
    0.0,    # Gods Finger is also unobtainable
    0.0    # Air is unobtainable, unless with the debug gamemode
]

def get_weapon() -> Item:
    return rng.choices(WEAPONS, WEAPON_RARITY)[0]

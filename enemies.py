from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from game import Game
from dataclasses import dataclass, field
from items import Item
import random

from constants import NAMES, WEAPONS

@dataclass
class Enemy:
    name: str = field(init=False)
    weapon: Item = field(init=False)

    def __post_init__(self) -> None:
        self.name = random.choice(NAMES)
        self.weapon = random.choice(WEAPONS)
    
    def AI(self, game: Type[Game]) -> None:
        ...
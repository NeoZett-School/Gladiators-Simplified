from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from game import Game
from dataclasses import dataclass, field
from items import Item
from enum import Enum
from constants import NAMES, RANDOM_SEED
from items import WEAPONS
import random

####################################################
# State machine works as a smart state familiarity #
#                                                  #
# ------------------------------------------------ #
# Agressive - Higher attack and attack rate        #
# Protective - Greater defenses, attacks less but  #
# also lowers chance to be attacked.               #
####################################################

rng = random.Random(RANDOM_SEED) # We literally use this everywhere, and it is a constant.

class StateMachine:
    @dataclass
    class State:
        this_attack_chance: float
        other_attack_chance: float

class EnemyState(Enum):
    AGGRESIVE = StateMachine.State(1.25, 1.0)
    PROTECTIVE = StateMachine.State(1.0, 0.75)

@dataclass
class Enemy:
    name: str = field(init=False)
    health: int = field(init=False)
    weapon: Item = field(init=False)
    state: EnemyState = field(init=False)

    def __post_init__(self) -> None:
        self.name = rng.choice(NAMES)
        self.weapon = rng.choice(WEAPONS)
    
    def attack(self, game) -> None:
        ...
    
    def damage_now(self) -> None:
        return self.weapon.damage_now()
from dataclasses import dataclass, field
from items import Item
from enum import Enum
from constants import NAMES, RANDOM_SEED, STATE_CHANGE
from items import get_weapon
import random

####################################################
# State machine works as a smart state familiarity #
#                                                  #
# ------------------------------------------------ #
# Agressive - Higher attack and attack rate        #
# Protective - Greater defenses, attacks less but  #
# also lowers chance to be attacked.               #
# Casual - Neglect any other state.
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
    CASUAL = StateMachine.State(1.0, 1.0)

@dataclass
class Enemy:
    name: str = field(init=False)
    health: int = field(init=False)
    weapon: Item = field(init=False)
    state: EnemyState = field(init=False)
    blood: int = field(init=False)
    blood_ticks: int = field(init=False)

    def __post_init__(self) -> None:
        self.name = rng.choice(NAMES)
        self.weapon = get_weapon()
        self.blood = 0
        self.blood_ticks = 0
    
    def apply_blood(self, action: Item, relevant_damage: int) -> None:
        if self.blood > 0:
            self.blood_ticks -= 1
            if self.blood_ticks <= 0:
                self.blood = 0
                self.blood_ticks = 0

        self.health = self.health - self.blood

        if relevant_damage > 0:
            self.blood = min(self.blood + action.blood, 5)
            self.blood_ticks = min(self.blood_ticks + action.blood_ticks, 3)
    
    def damage_now(self, variable_chance: float = 1.0) -> int:
        self.state = rng.choices((self.state, EnemyState.CASUAL, EnemyState.PROTECTIVE, EnemyState.AGGRESIVE), STATE_CHANGE)[0]
        return int(self.weapon.damage_now(self.state.value.this_attack_chance * variable_chance))
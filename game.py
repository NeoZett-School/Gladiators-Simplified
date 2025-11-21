from typing import List, Dict, TypeVar, Callable, Generic, ValuesView, Optional, Any
from colorama import init as colorama_init, Fore, Back, Style
from dataclasses import dataclass, field
from translator import Transcriber, Language
from playsound3.playsound3 import Sound
from playsound3 import playsound
from enum import Enum
from items import Item, get_weapon
from enemies import Enemy, EnemyState
from achievements import Achievement, ACHIEVEMENTS
import constants
import random
import msvcrt
import time
import sys
import os

# ---- Initialization ----

if __name__ != "__main__": 
    sys.exit() # We are importing the script

print("Loading...")

colorama_init() # We'll initialize the colorama module

def clear_screen(): # Create a method to clear the screen
    if os.name == "nt":
        os.system("cls") # Windows
    else: os.system("clear") # Linux / Macbook

def draw_title(*text: str) -> None: # We'll create a title method to render all title firstly for every page
    clear_screen()
    print(*text, end="\n\n")

# We'll manifacture the drop down menu
def menu(title: str, prompt: str, options: Dict[str, str]):
    print(title)
    for k, v in options.items():
        print(Fore.BLUE + k + ": " + Fore.RESET + v)
    return input(prompt)

# We'll create a method to run a new background sound
def create_background_music() -> Sound:
    return playsound("./sounds/background.mp3", False)

rng = random.Random(constants.RANDOM_SEED) # We literally use this everywhere, and it is a constant.

# ---- Settings ----

# We'll create a type var for typing, when it is dynamic and not directly static
SettingType = TypeVar("SettingType", bound=Any)

# We'll create a dataclass for a setting
@dataclass
class Setting(Generic[SettingType]):
    value: SettingType
    toggle: bool = field(default=False)
    custom_logic: Callable[..., Any] = field(default=lambda: None)
    enum: "Settings" = field(init=False)

# We'll create a enum for different settings
class Settings(Enum):
    GORE: Setting[bool] = Setting(False) # Wheter we express bloddy and visious imaginary text
    MUSIC: Setting[bool] = Setting(True, toggle=True, custom_logic=lambda: Game.toggle_music())

    @classmethod
    def load(cls) -> None: # Load all settings so they appeal to their real object
        for v in cls.__members__.values():
            if isinstance(v.value, Setting):
                v.value.enum = v

    @classmethod
    def all(cls) -> ValuesView[Setting]: # Get all settings
        return cls.__members__.values()
    
    @property
    def setting(self) -> Setting: # Get the setting object, with the given value
        return object.__getattribute__(self, "_value_")
    
    @property
    def name(self) -> str: # The name will be the capitalization of that of the real enum name
        return object.__getattribute__(self, "_name_").capitalize()

    @property
    def value(self) -> SettingType: # Get the real value in the setting
        return self.setting.value
    
    @property
    def toggle(self) -> bool:
        return self.setting.toggle
    
    @property
    def text_value(self) -> str: # Get the text correspondance of the value
        if isinstance(self.value, bool):
            return transcriber.get_index(13) if self.value else transcriber.get_index(14)

    def handle_input(self, text: str) -> None: # Handle text input.
        if isinstance(self.value, bool):
            if self.toggle:
                self.setting.value = not self.value
                self.setting.custom_logic()
                return
            on_text, off_text = transcriber.get_index(13).lower().strip(), transcriber.get_index(14).lower().strip()
            self.setting.value = text.lower().strip() in (on_text[0], on_text) and not text in (off_text[0], off_text)

# ---- Game ----

class Game: # Create a namespace for our game
    player_name: str = "" # The player name
    difficulty: int = 1
    active: bool = False # Wheter the game is actively running or not

    health: int = 25
    weapons: List[Item] = [
        get_weapon()
    ]

    background_music: Sound
    enemy: Enemy = None
    round: int = 1

    player_damage_cache: int = 0.0 # Smart auto balancing!
    enemy_damage_cache: int = 0.0

    loses: int = 0
    wins: int = 0

    has_first_game_achievement: bool = False
    has_trident_achivement: bool = False
    has_win_achivement: bool = False
    has_inventory_achievement: bool = False
    has_round_ten_achivement: bool = False
    has_lose_five_achivement: bool = False
    has_win_five_achivement: bool = False

    scenery: float = 100.0 # You begin with hundred scenery points.

    achievements: List[Achievement] = []

    log: str = None

    def toggle_music() -> None:
        if Game.background_music:
            Game.background_music.stop()
            Game.background_music = None
        else: 
            Game.background_music = create_background_music()

    def menu() -> None: # Start rendering the menu
        draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(1).upper() + Style.RESET_ALL)
        directory = menu(
            title = transcriber.get_index(5), 
            prompt = transcriber.get_index(6), 
            options = {
                "1": transcriber.get_index(7),
                "2": transcriber.get_index(8),
                "3": transcriber.get_index(33),
                "4": transcriber.get_index(9)
            }
        ).lower().strip()
        match directory: # do something depending on the input
            case "1":
                Game.game()
            case "2":
                Game.options()
            case "3":
                Game.stats()
            case "4":
                sys.exit()
        Game.menu() # We'll just restart the menu if we don't enter anything valid
    
    def options() -> None: # Start rendering the options
        draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(2).upper() + Style.RESET_ALL)

        options: Dict[str, str] = {}
        settings: Dict[str, Settings] = {}
        for i, v in enumerate(Settings.all()): # We'll generate all the options before we can use them in the menu
            i = str(i + 1)
            settings[i] = v
            options[i] = v.name + f" [{Fore.MAGENTA}{v.text_value}{Style.RESET_ALL}]"

        setting_name = menu(
            title = transcriber.get_index(10),
            prompt = transcriber.get_index(11),
            options = options
        ).lower().strip()

        setting = settings.get(
            setting_name.lower().strip()
        )
        if not setting: # We'll exit the settings if the setting was incorrect
            return
        if not setting.toggle:
            setting.handle_input(input(transcriber.get_index(12)))
        else: setting.handle_input("")
        Game.options()
    
    def stats() -> None:
        draw_main_title()
        print(transcriber.get_index(33))
        print()
        if len(Game.achievements) > 0:
            for achievement in Game.achievements:
                print(achievement.text)
        else: print(transcriber.get_index(34))
        print()
        print(transcriber.get_index(35))
        msvcrt.getch()
    
    def game() -> None: # We'll handle the actual game logic here
        Game.active = True
        while Game.active:
            draw_main_title()
            Game.battle()
    
    def render_game() -> None:
        print(
            transcriber.get_index(21, 26)\
                .replace("player_name", Game.player_name)\
                .replace("enemy_name", Game.enemy.name)\
                .replace("game_round", str(Game.round))\
                .replace("player_health", str(Game.health))\
                .replace("enemy_health", str(Game.enemy.health))
        )
        print()

        if Game.log:
            print(Game.log)
            print()
    
    def battle() -> Optional[bool]:
        if not Game.has_first_game_achievement:
            Game.achievements.append(ACHIEVEMENTS["First Game"])
            Game.has_first_game_achievement = True
        
        if not Game.has_round_ten_achivement:
            Game.achievements.append(ACHIEVEMENTS["Round Ten"])
            Game.has_round_ten_achivement = True
        
        if not Game.has_inventory_achievement and len(Game.weapons) >= 5:
            Game.achievements.append(ACHIEVEMENTS["Inventory At Large"])
            Game.has_inventory_achievement = True
        
        if not Game.enemy:
            Game.enemy = Enemy()
            Game.enemy.health = 25
            Game.enemy.state = EnemyState.CASUAL
        
        Game.render_game()

        options: Dict[str, Item] = {}
        for i, weapon in enumerate(Game.weapons):
            options[str(i+1)] = weapon

        retreat = str(len(options) + 1)

        action_name = menu(
            title = transcriber.get_index(16),
            prompt = transcriber.get_index(17),
            options = {k: v.name for k, v in options.items()} | ({retreat: "Retreat"} if Game.enemy.health < 8 or Game.difficulty == 0 else {})
        ).lower().strip()

        draw_main_title()

        print(transcriber.get_index(18))

        if action_name == retreat:
            Game.log = transcriber.get_index(35)
            for weapon in Game.weapons[:]:
                if len(Game.weapons) == 1: break
                if rng.random() < (0.75 if Game.difficulty == 0 else 0.25):
                    Game.weapons.remove(weapon)
            Game.reset()
            return

        action = options.get(action_name)

        if not action:
            Game.active = False
            return
        
        if action.name == "Trident" and not Game.has_trident_achivement:
            Game.achievements.append(ACHIEVEMENTS["The Power Of The Trident"])
            Game.has_trident_achivement = True

        # helper
        def clamp(x, lo, hi):
            return max(lo, min(hi, x))

        # small epsilon to avoid division by zero if both caches are zero
        EPS = 1e-6

        # Normalized "who is ahead" metric in [0,1]
        #  - 0.0 => player has done 0 damage and enemy dominated (player factor minimal)
        #  - 0.5 => balanced
        #  - 1.0 => player has done all the damage (enemy factor minimal)
        total = Game.player_damage_cache + Game.enemy_damage_cache + EPS
        player_share = Game.player_damage_cache / total   # in (0,1)
        # We want player_factor such that when player_share is 0.5, factor is 0.5
        # and when player_share is high, player_factor reduces enemy's chance (or vice versa).
        player_factor = clamp(1.0 - player_share, 0.0, 1.0)
        enemy_factor = clamp(1.0 - player_factor, 0.0, 1.0)  # equals player_share, but kept explicit

        # drift: base between 1.05 and 1.35 (same distribution as 1.35 - rng.random()*0.30)
        base_drift = 1.35 - rng.random() * 0.30

        # difficulty modifiers (explicit)
        if Game.difficulty == 0 or player_factor >= 0.75:      # easy
            player_diff_mod = +0.05
            enemy_diff_mod  = -0.05
        elif Game.difficulty == 2 or enemy_factor >= 0.75:    # hard
            player_diff_mod = -0.05
            enemy_diff_mod  = +0.05
        else:                        # normal (1)
            player_diff_mod = 0.0
            enemy_diff_mod  = 0.0

        player_drift = base_drift + player_diff_mod
        # recompute base for enemy separately so RNG affects both independently (like your original)
        enemy_drift = 1.35 - rng.random() * 0.30 + enemy_diff_mod

        # Compose variable chances and clamp to [0.0, 1.0]
        player_variable_chance = clamp(Game.enemy.state.value.other_attack_chance * player_drift, 0.0, 1.0)
        enemy_variable_chance  = clamp(enemy_drift, 0.0, 1.0)

        # difficulty multipliers for final damage output (explicit)
        player_damage_mult = 1.15 if Game.difficulty == 0 else 0.85 if Game.difficulty == 2 else 1.0
        enemy_damage_mult  = 0.85 if Game.difficulty == 0 else 1.15 if Game.difficulty == 2 else 1.0

        player_damage = int(action.damage_now(player_variable_chance) * player_damage_mult)
        enemy_damage  = int(Game.enemy.damage_now(enemy_variable_chance) * enemy_damage_mult)

        Game.player_damage_cache = Game.player_damage_cache * 0.8 + player_damage * 0.2
        Game.enemy_damage_cache  = Game.enemy_damage_cache * 0.8 + enemy_damage * 0.2
        Game.scenery *= action.scenery

        Game.health = Game.health - enemy_damage
        Game.enemy.health = Game.enemy.health - player_damage

        Game.log = f"| Log\n{transcriber.get_index(19, 21)\
                            .replace("player_damage", str(player_damage))\
                            .replace("action_name", action.name)\
                            .replace("enemy_damage", str(enemy_damage))\
                            .replace("enemy_weapon", Game.enemy.weapon.name)}"

        player_dead = Game.health <= 0
        enemy_dead = Game.enemy.health <= 0

        if all((player_dead, enemy_dead)):
            if rng.random() < (0.45 if Game.difficulty == 0 else 0.25):
                Game.win()
            else:
                Game.loss()
        elif player_dead:
            Game.loss()
        elif enemy_dead:
            Game.win()

        time.sleep(max(rng.random() * 1, 0.5))

        Game.round += 1
    
    def loss() -> None:
        Game.loses += 1
        if not Game.has_lose_five_achivement and Game.loses >= 5:
            Game.achievements.append(ACHIEVEMENTS["Lose Five"])
            Game.has_lose_five_achivement = True

        time.sleep(0.25)
        draw_main_title()

        print(transcriber.get_index(26))

        print(transcriber.get_index(27) + "\r", end="")

        second_chance = rng.random() < Game.scenery * (0.75 if Game.difficulty == 2 else 1.25 if Game.difficulty == 0 else 1.0)

        time.sleep(max(rng.random() * 10, 2))

        if second_chance:
            print(transcriber.get_index(27) + transcriber.get_index(28))
        else:
            print(transcriber.get_index(27) + transcriber.get_index(29))
            Game.weapons = [
                get_weapon()
            ]

        Game.log = f"| Log\n{transcriber.get_index(30)}{transcriber.get_index(31) if second_chance else ""}"

        time.sleep(5.0)
        Game.reset()
    
    def win() -> None:
        Game.wins += 1

        if not Game.has_win_achivement:
            Game.achievements.append(ACHIEVEMENTS["First Win"])
            Game.has_win_achivement = True
        
        if not Game.has_win_five_achivement and Game.wins >= 5:
            Game.achievements.append(ACHIEVEMENTS["Win Five"])
            Game.has_win_five_achivement = True

        Game.log = "| Log\n" + transcriber.get_index(32)
        if not Game.enemy.weapon in Game.weapons:
            Game.weapons.append(Game.enemy.weapon)
        Game.reset()
    
    def reset() -> None:
        Game.player_damage_cache = 0
        Game.enemy_damage_cache = 0
        Game.enemy = None
        Game.health = 25
        Game.round = 1

# ------ Settings ------

# Loadin...
Settings.load()

# ---- Language ----

lang = ""
while not Language.get(lang):
    draw_title(Fore.CYAN + Style.BRIGHT + "GLADIATORS" + Style.RESET_ALL)
    print("Languages:")
    for lang in Language.iterate():
        print(lang.value.name)
    print()
    lang = input("Select one language (f.e 'sv'): ")
transcriber = Transcriber(Language.get(lang))
draw_main_title = lambda: draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(0) + Style.RESET_ALL)

# ---- Introduction ----

while not Game.player_name:
    draw_main_title()
    Game.player_name = input(transcriber.get_index(3)) # Select a name

difficulty = ""
while not difficulty in ("0", "1", "2"):
    draw_main_title()
    difficulty = input(transcriber.get_index(15))
Game.difficulty = int(difficulty)

draw_main_title()

print(transcriber.get_index(4))
for i in range(10): # We'll make a small loading scene
    print(f"\r[{Fore.GREEN + Style.BRIGHT}{"-"*i}{Style.RESET_ALL + Fore.YELLOW}{"-"*(10-i)}{Style.RESET_ALL}]", end="")
    time.sleep(0.12)

# ---- Start the game ----

Game.background_music = create_background_music()
Game.menu()
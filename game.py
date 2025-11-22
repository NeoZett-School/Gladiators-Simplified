from typing import List, Dict, TypeVar, Callable, Generic, ValuesView, Optional, Any
from colorama import init as colorama_init, Fore, Back, Style
from dataclasses import dataclass, field
from translator import Transcriber, Language
from playsound3.playsound3 import Sound
from playsound3 import playsound
from enum import Enum
from items import Item, WEAPONS, WEAPON_RARITY, get_weapon
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
def prompt_menu(title: str, prompt: str, options: Dict[str, str]):
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

    currency: int = 0
    lifetime_currency: int = 0

    player_damage_cache: float = 0.0 # Smart auto balancing!
    enemy_damage_cache: float = 0.0

    total_rounds: int = 0
    loses: int = 0
    wins: int = 0

    blood: int = 0
    blood_ticks: int = 0

    has_first_game_achievement: bool = False
    has_trident_achievement: bool = False
    has_win_achievement: bool = False
    has_inventory_achievement: bool = False
    has_round_ten_achievement: bool = False
    has_lose_five_achievement: bool = False
    has_win_five_achievement: bool = False
    has_sell_achievement: bool = False
    has_buy_achievement: bool = False
    has_reavers_pike_achievement: bool = False
    has_axe_achievement: bool = False

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
        while True:
            draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(1).upper() + Style.RESET_ALL)
            print((f"{Fore.RED}HARD{Fore.RESET}" if Game.difficulty == 2 else f"{Fore.BLUE}NORMAL{Fore.RESET}" if Game.difficulty == 1 else f"{Fore.GREEN}EASY{Fore.RESET}" if Game.difficulty == 0 else f"{Fore.MAGENTA}EXPERIMENTAL{Fore.RESET}"))
            print()
            print(rng.choice(constants.INFO_TEXT))
            print()
            print(f"{Style.DIM}Makaronies are your unit of comparison.{Style.RESET_ALL}")
            print(f"{Game.lifetime_currency} Makaronies earned in total")
            print(f"{Game.total_rounds} Total rounds")
            print(f"{Game.wins} Wins")
            print(f"{Game.loses} Loses")
            print()
            directory = prompt_menu(
                title = transcriber.get_index(5), 
                prompt = transcriber.get_index(6), 
                options = {
                    "1": transcriber.get_index(7),
                    "2": transcriber.get_index(8),
                    "3": transcriber.get_index(33),
                    "4": transcriber.get_index(37),
                    "5": transcriber.get_index(38),
                    "6": transcriber.get_index(9)
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
                    Game.shop()
                case "5":
                    Game.trader()
                case "6":
                    sys.exit()
    
    def options() -> None: # Start rendering the options
        while True:
            draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(2).upper() + Style.RESET_ALL)

            options: Dict[str, str] = {}
            settings: Dict[str, Settings] = {}
            for i, v in enumerate(Settings.all()): # We'll generate all the options before we can use them in the menu
                i = str(i + 1)
                settings[i] = v
                options[i] = v.name + f" [{Fore.MAGENTA}{v.text_value}{Style.RESET_ALL}]"

            setting_name = prompt_menu(
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
    
    def shop() -> None:
        while True:
            draw_main_title()
            print(f"{Game.currency} Makaronies")
            print()
            costs = {}
            weapons = {}
            menu_options = {}

            total_weights = sum(WEAPON_RARITY) or 1
            for i, weapon in enumerate(WEAPONS):
                ident = str(i + 1)
                weight = WEAPON_RARITY[WEAPONS.index(weapon)]
                prob = weight / total_weights
                rarity_multiplier = 1.0 - prob  # rarer -> larger multiplier
                # ensure the weapon object has .rarity, .blood, .blood_ticks attributes
                rarity_reward = constants.RARITY_REWARD.get(getattr(weapon, "rarity", "common"), 0)
                blood_spill = ((weapon.damage + getattr(weapon, "blood", 0) * getattr(weapon, "blood_ticks", 0)) / 2)
                # clamp/scaling for stability
                base = max(0.0, blood_spill * weapon.damage_chance * weapon.scenery)
                reward = int(rarity_multiplier * base * 100) + rarity_reward
                cost = max(1, reward * 10)

                # only display purchasable weapons (or filter designer chooses)
                if weapon.rarity == "experimental": continue
                costs[ident] = cost
                weapons[ident] = weapon
                affordable = Game.currency >= cost
                menu_options[ident] = f"{constants.RARITY_COLOR.get(weapon.rarity)}{weapon.name}{Style.RESET_ALL} " \
                                    f"({weapon.damage} dmg, {weapon.damage_chance:.2f} hit, bleed {getattr(weapon,'blood',0)}x{getattr(weapon,'blood_ticks',0)}) - " \
                                    f"{Style.BRIGHT}{Fore.GREEN if affordable else Fore.RED}{cost} Makaronies{Style.RESET_ALL}"
                    
            purchase_name = prompt_menu(
                title = transcriber.get_index(37),
                prompt = transcriber.get_index(17),
                options = menu_options
            ).lower().strip()
            
            purchase_weapon = weapons.get(purchase_name)
            purchase_cost = costs.get(purchase_name)
            
            if not purchase_weapon:
                return
            
            if Game.currency >= purchase_cost:
                Game.weapons.append(purchase_weapon)
                Game.currency -= purchase_cost

                if not Game.has_buy_achievement:
                    Game.achievements.append(ACHIEVEMENTS["Buy"])
                    Game.has_buy_achievement = True
    
    def trader() -> None:
        while True:
            draw_main_title()
            print(f"{Game.currency} Makaronies")
            print()

            if len(Game.weapons) <= 1:
                print(transcriber.get_index(39))
                msvcrt.getch()
                return

            gives = {}
            weapons = {}
            menu_options = {}

            total_weights = sum(WEAPON_RARITY) or 1
            for i, weapon in enumerate(Game.weapons):
                ident = str(i + 1)
                weight = WEAPON_RARITY[i]
                prob = weight / total_weights
                rarity_multiplier = 1.0 - prob  # rarer -> larger multiplier
                # ensure the weapon object has .rarity, .blood, .blood_ticks attributes
                rarity_reward = constants.RARITY_REWARD.get(getattr(weapon, "rarity", "common"), 0)
                blood_spill = ((weapon.damage + getattr(weapon, "blood", 0) * getattr(weapon, "blood_ticks", 0)) / 2)
                # clamp/scaling for stability
                base = max(0.0, blood_spill * weapon.damage_chance * weapon.scenery)
                reward = int(rarity_multiplier * base * 100) + rarity_reward
                cost = max(1, reward * 10)
                give = int(cost / 2)

                # only display purchasable weapons (or filter designer chooses)
                gives[ident] = give
                weapons[ident] = weapon
                menu_options[ident] = f"{constants.RARITY_COLOR.get(weapon.rarity)}{weapon.name}{Style.RESET_ALL} " \
                                    f"({weapon.damage} dmg, {weapon.damage_chance:.2f} hit, bleed {getattr(weapon,'blood',0)}x{getattr(weapon,'blood_ticks',0)}) - " \
                                    f"{give} Makaronies"
                    
            trade_name = prompt_menu(
                title = transcriber.get_index(38),
                prompt = transcriber.get_index(17),
                options = menu_options
            ).lower().strip()
            
            trade_weapon = weapons.get(trade_name)
            trade_gives = gives.get(trade_name)
            
            if not trade_weapon:
                return
            
            # confirm
            draw_main_title()
            print(transcriber.get_index(40).replace("trade_gives", str(trade_gives)).replace("trade_name", trade_weapon.name))
            resp = input("> ").strip().lower()
            if resp not in ("y", "yes"):
                continue  # return to trader menu
            
            Game.weapons.remove(trade_weapon)
            Game.currency += trade_gives

            if not Game.has_sell_achievement:
                Game.achievements.append(ACHIEVEMENTS["Sell"])
                Game.has_sell_achievement = True
    
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
                .replace("enemy_health", str(Game.enemy.health))\
                .replace("player_blood", f"{Game.blood}x{Game.blood_ticks}")\
                .replace("enemy_blood", f"{Game.enemy.blood}x{Game.enemy.blood_ticks}")
        )
        print()

        if Game.log:
            print(Game.log)
            print()
    
    def battle() -> Optional[bool]:
        if not Game.has_first_game_achievement:
            Game.achievements.append(ACHIEVEMENTS["First Game"])
            Game.has_first_game_achievement = True
        
        if not Game.has_round_ten_achievement and Game.round >= 10:
            Game.achievements.append(ACHIEVEMENTS["Round Ten"])
            Game.has_round_ten_achievement = True
        
        if not Game.has_inventory_achievement and len(Game.weapons) >= 5:
            Game.achievements.append(ACHIEVEMENTS["Inventory At Large"])
            Game.has_inventory_achievement = True
        
        if not Game.has_reavers_pike_achievement and any(weapon.name == "Reavers Pike" for weapon in Game.weapons):
            Game.achievements.append(ACHIEVEMENTS["Reavers Pike"])
            Game.has_reavers_pike_achievement = True
        
        if not Game.has_axe_achievement and any(weapon.name == "Axe" for weapon in Game.weapons):
            Game.achievements.append(ACHIEVEMENTS["Axe"])
            Game.has_axe_achievement = True

        if not Game.enemy:
            Game.enemy = Enemy()
            Game.enemy.health = 25
            Game.enemy.state = EnemyState.CASUAL
        
        Game.render_game()

        options: Dict[str, Item] = {}
        for i, weapon in enumerate(Game.weapons):
            options[str(i+1)] = weapon

        retreat = str(len(options) + 1)

        action_name = prompt_menu(
            title = transcriber.get_index(16),
            prompt = transcriber.get_index(17),
            options = {k: f"{constants.RARITY_COLOR[v.rarity]}{v.name}{Style.RESET_ALL}" for k, v in options.items()} | ({retreat: "Retreat"} if Game.enemy.health < 8 or Game.difficulty == 0 else {})
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
        
        if action.name == "Trident" and not Game.has_trident_achievement:
            Game.achievements.append(ACHIEVEMENTS["The Power Of The Trident"])
            Game.has_trident_achievement = True

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

        if Game.blood:
            Game.blood_ticks -= 1
            if Game.blood_ticks <= 0:
                Game.blood = 0
                Game.blood_ticks = 0

        Game.health = Game.health - enemy_damage - Game.blood
        Game.enemy.health = Game.enemy.health - player_damage
        Game.enemy.apply_blood(action, player_damage) # Does the exact same thing, but for the enemy

        if enemy_damage > 0:
            Game.blood = min(Game.blood + Game.enemy.weapon.blood, 5)
            Game.blood_ticks = min(Game.blood_ticks + Game.enemy.weapon.blood_ticks, 3)

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
        Game.total_rounds += 1
    
    def loss() -> None:
        Game.loses += 1
        if not Game.has_lose_five_achievement and Game.loses >= 5:
            Game.achievements.append(ACHIEVEMENTS["Lose Five"])
            Game.has_lose_five_achievement = True

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
            if not Game.difficulty == 3:
                for weapon in Game.weapons[:]:
                    if not weapon.name == "Reavers Pike":
                        Game.weapons.remove(weapon)
                Game.weapons.append(get_weapon())

        Game.log = f"| Log\n{transcriber.get_index(30)}{transcriber.get_index(31) if second_chance else ""}"

        time.sleep(5.0)
        Game.reset()
    
    def win() -> None:
        Game.wins += 1

        if not Game.has_win_achievement:
            Game.achievements.append(ACHIEVEMENTS["First Win"])
            Game.has_win_achievement = True
        
        if not Game.has_win_five_achievement and Game.wins >= 5:
            Game.achievements.append(ACHIEVEMENTS["Win Five"])
            Game.has_win_five_achievement = True
        
        weight = WEAPON_RARITY[WEAPONS.index(Game.enemy.weapon)]
        total = sum(WEAPON_RARITY) or 1
        prob = weight / total
        rarity_multiplier = 1.0 - prob  # in [0,1]
        rarity_reward = constants.RARITY_REWARD[Game.enemy.weapon.rarity]
        blood_spill = ((Game.enemy.weapon.damage + Game.enemy.weapon.blood * Game.enemy.weapon.blood_ticks) / 2)
        reward = int(rarity_multiplier * blood_spill * Game.enemy.weapon.damage_chance * Game.enemy.weapon.scenery * 100) + rarity_reward
        reward = max(0, reward)
        Game.currency += reward
        Game.lifetime_currency += reward

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

        Game.final()
    
    def final() -> None:
        # Big block of conditions
        # Round condition
        needed_rounds = (200 if Game.difficulty == 2 else 50 if Game.difficulty == 0 else 100)
        if not Game.total_rounds >= needed_rounds: return
        # Win/Loss condition
        if not Game.wins >= 10: return
        if not Game.loses >= 5: return
        # Achievement condition (You must have explored the game a little, easy)
        if not len(Game.achievements) >= 7: return
        # Inventory conditions
        if not any(weapon.name == "Reavers Pike" for weapon in Game.weapons): return
        if not len(Game.weapons) >= 3: return
        # Currency condition
        if not (Game.lifetime_currency > 500 and Game.currency > 2000): return

        # Final screen
        draw_main_title()
        print("=== Final Statistics ===")
        print(f"Player: {Game.player_name}")
        print(f"Difficulty: {Game.difficulty} (0=Easy, 1=Normal, 2=Hard, 09=Experimental)") # This is the first time we reference the forth game mode. Only now will the player now.
        print(f"Total rounds: {Game.total_rounds}")
        print(f"Wins: {Game.wins}  |  Losses: {Game.loses}")
        print(f"Makaronies (current / lifetime from battle): {Game.currency} / {Game.lifetime_currency}")
        print(f"Weapons kept: {', '.join(w.name for w in Game.weapons)}")
        # optional: list achievements
        print("Achievements unlocked:")
        for a in Game.achievements:
            print(" -", a.name if hasattr(a, "name") else getattr(a, "text", str(a)))
        print()
        print(transcriber.get_index(41, 50).replace("rounds_needed", str(needed_rounds)))
        print()
        print("Press any key to continue.")
        msvcrt.getch()
        draw_main_title()
        print("Thank you for playing! This was a simple school project to begin with, and spiraled into something else.")
        print()
        print("This game was developed and created by: Neo Zetterberg")
        print("And was made at late 2025.")
        print()
        print("Press any key to continue.")
        msvcrt.getch()
        draw_main_title()
        win_factor = (Game.wins / Game.loses)
        difficulty_factor = (Game.difficulty if Game.difficulty > 0 else 0.5)
        achievements_factor = (len(Game.achievements) / len(ACHIEVEMENTS))
        currency_factor = Game.currency / Game.lifetime_currency
        factor = win_factor * difficulty_factor * achievements_factor * currency_factor
        print(f"Your score for this round was: {min(int((factor/3.0) * 10), 10)}/10")
        if factor <= 0.5:
            print("Don't worry. It didn't go very well, but we still believe next time will be even better!")
        elif factor <= 0.75:
            print("One more time, and you will do even better!")
        elif factor <= 1.25:
            print("Okay, maybe not perfect, but it is really good. Time to up the difficulty!")
        elif factor <= 1.75:
            print("We are not sure how you did it, but you are over the normal!")
        elif factor <= 2.5:
            print("Incredible, just incredible. Continue that way.")
        else:
            print("Perfect.")
        print()
        print("Press any key to exit.")
        msvcrt.getch()
        sys.exit(0)

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
while not difficulty in ("0", "1", "2", "09"):
    draw_main_title()
    difficulty = input(transcriber.get_index(15))
Game.difficulty = int(difficulty)

if difficulty == "09":
    Game.weapons.clear()
    Game.weapons = WEAPONS.copy()

    Game.has_first_game_achievement = True
    Game.has_trident_achievement = True
    Game.has_win_achievement = True
    Game.has_inventory_achievement = True
    Game.has_round_ten_achievement = True
    Game.has_lose_five_achievement = True
    Game.has_win_five_achievement = True
    Game.has_sell_achievement = True
    Game.has_buy_achievement = True
    Game.has_reavers_pike_achievement = True
    Game.has_axe_achievement = True
    Game.achievements = list(ACHIEVEMENTS.values())

draw_main_title()

print(transcriber.get_index(4))
print()
print(rng.choice(constants.INFO_TEXT))
for i in range(10): # We'll make a small loading scene
    print(f"\r[{Fore.GREEN + Style.BRIGHT}{"-"*i}{Style.RESET_ALL + Fore.YELLOW}{"-"*(10-i)}{Style.RESET_ALL}]", end="")
    time.sleep(0.25)

# ---- Start the game ----

Game.background_music = create_background_music()
Game.menu()
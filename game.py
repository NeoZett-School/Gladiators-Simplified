from typing import List, Dict, TypeVar, Generic, ValuesView, Any
from colorama import init as colorama_init, Fore, Back, Style
from dataclasses import dataclass, field
from translator import Transcriber, Language
from playsound3.playsound3 import Sound
from playsound3 import playsound
from enum import Enum
from items import Item, WEAPONS
from enemies import Enemy
import constants
import random
import time
import sys
import os

# ---- Initialization ----

if __name__ != "__main__": 
    sys.exit() # We are importing the script

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
def background_sound() -> Sound:
    return playsound("./sounds/background.mp3", False)

rng = random.Random(constants.RANDOM_SEED) # We literally use this everywhere, and it is a constant.

# ---- Settings ----

# We'll create a type var for typing, when it is dynamic and not directly static
SettingType = TypeVar("SettingType", bound=Any)

# We'll create a dataclass for a setting
@dataclass
class Setting(Generic[SettingType]):
    value: SettingType
    enum: "Settings" = field(init=False)

# We'll create a enum for different settings
class Settings(Enum):
    GORE: Setting[bool] = Setting(False) # Wheter we express bloddy and visious imaginary text

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
    def text_value(self) -> str: # Get the text correspondance of the value
        if isinstance(self.value, bool):
            return transcriber.get_index(13) if self.value else transcriber.get_index(14)

    def handle_input(self, text: str) -> None: # Handle text input.
        if isinstance(self.value, bool):
            on_text, off_text = transcriber.get_index(13).lower().strip(), transcriber.get_index(14).lower().strip()
            self.setting.value = text.lower().strip() in (on_text[0], on_text) and not text in (off_text[0], off_text)

# ---- Game ----

class Game: # Create a namespace for our game
    player_name: str = "" # The player name
    difficulty: int = 1
    active: bool = False # Wheter the game is actively running or not

    health: int = 100
    weapons: List[Item] = [
        rng.choice(WEAPONS)
    ]

    background_music: Sound
    enemy: Enemy

    def menu() -> None: # Start rendering the menu
        draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(1).upper() + Style.RESET_ALL)
        directory = menu(
            title = transcriber.get_index(5), 
            prompt = transcriber.get_index(6), 
            options = {
                "1": transcriber.get_index(7),
                "2": transcriber.get_index(8),
                "3": transcriber.get_index(9)
            }
        ).lower().strip()
        match directory: # do something depending on the input
            case "1":
                Game.game()
            case "2":
                Game.options()
            case "3":
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
        setting.handle_input(input(transcriber.get_index(12)))
        Game.options()
    
    def game() -> None: # We'll handle the actual game logic here
        Game.active = True
        while Game.active:
            draw_main_title()
            Game.battle()
    
    def render_game() -> None:
        print(f"Your health: {Game.health}/100")
        print(f"Enemy health: {""}")
    
    def battle() -> None:
        
        action = menu(
            title = transcriber.get_index(17),
            prompt = transcriber.get_index(18),
            options = {}
        ).lower().strip()

# ---- Settings ----

# Loadin
for obj in Game.__dict__.values(): # Load the namespace to be according to programming standards
    if callable(obj): obj = staticmethod(obj)
Settings.load()

# ---- meta options ----

# We have these options because of how our settings menu is made. 
# It is not togglable, but anything that requires a setting will still be set there.
draw_title(Fore.CYAN + Style.BRIGHT + "GLADIATORS" + Style.RESET_ALL)
print(Style.DIM + "Read the documentation for a full comprehensive list of meta-options\nLeave this field empty if you want the casual experience\n" + Style.RESET_ALL)
game_options_input = input("Select game options (f.e 'no music, no name, ...') ").lower().split(",")
game_options = []
for option in game_options_input:
    game_options.append(option.strip())

Game.background_music = background_sound()

if "no music" in game_options:
    Game.background_music.stop()

# ---- Language ----

lang = ""
while not Language.get(lang):
    draw_title(Fore.CYAN + Style.BRIGHT + "GLADIATORS" + Style.RESET_ALL)
    print("Languages:")
    for lang in Language.iterate():
        print(lang.value.name)
    print()
    lang = input("Select one language: ")
transcriber = Transcriber(Language.get(lang))
draw_main_title = lambda: draw_title(Fore.CYAN + Style.BRIGHT + transcriber.get_index(0) + Style.RESET_ALL)

# ---- Introduction ----

if "no name" in game_options:
    Game.player_name = "Unknown"
else:
    while not Game.player_name:
        draw_main_title()
        Game.player_name = input(transcriber.get_index(3)) # Select a name

difficulty = ""
while not difficulty in ("0", "1", "2"):
    draw_main_title()
    difficulty = input(transcriber.get_index(15))
Game.difficulty = int(difficulty)

draw_main_title()

print("\n" + transcriber.get_index(4))
for i in range(10): # We'll make a small loading scene
    print(f"\r[{Fore.GREEN + Style.BRIGHT}{"-"*i}{Style.RESET_ALL + Fore.YELLOW}{"-"*(10-i)}{Style.RESET_ALL}]", end="")
    time.sleep(0.12)

# ---- Start the game ----

Game.menu()
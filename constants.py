from colorama import Fore

class LANGUAGE:
    """Basic configuration for the language."""
    BASE_PATH = "./languages"
    EXTENTION = ".lng"

NAMES = [
    "Alisa",
    "Faur",
    "Likare"
]

RARITY_COLOR = {
    "common": Fore.GREEN,
    "uncommon": Fore.CYAN,
    "rare": Fore.MAGENTA,
    "legendary": Fore.RED,
    "experimental": Fore.YELLOW
}

RARITY_REWARD = {
    "common": 10,
    "uncommon": 20,
    "rare": 50,
    "legendary": 100,
    "experimental": 500
}

RANDOM_SEED = None
STATE_CHANGE = (1.0, 0.15, 0.05, 0.02)
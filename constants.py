from colorama import Fore

class LANGUAGE:
    """Basic configuration for the language."""
    BASE_PATH = "./languages"
    EXTENTION = ".lng"

NAMES = [
    "Alisa",
    "Faur",
    "Likare",
    "Goblin",
    "Dragon Of Askarin",
    "Smuglin",
    "Cooper",
    "Nightmare",
    "The Thieves of The Graveyard",
    "Tamil",
    "Karel",
    "Tora",
    "Tarim",
    "Ant Atom"
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

LOADING_TEXT = [
    "Did you know that you cant lose the reavers pike?",
    "You can sell bad items to the trader and recieve half the price.",
    "Green is common, blue is uncommon, magenta is rare and red are legendary.",
    "Buy the reavers pike, and never lose it.",
    "One achievement requires you to use the trident",
    "Get five items and you will get an achievement",
    "There is a secret game modes, only the developers know of.",
    "The escalibur is very powerful, deals 20 damage, but is very unlikely to hit.",
    "The reavers pike is half as common as the escalibur.",
    "The axe has a 95%% chance to hit.",
    "You can always retreat if you play on easy mode.",
    "The costs and earnings after every battle is carefully calculated based on how powerful the item is.",
    "Even if you lose, you are lucky to get 5 loses, which gives you an award!",
    "Win five times to get an award!",
    "The name of every enemy is generated randomly."
]

RANDOM_SEED = None
STATE_CHANGE = (1.0, 0.15, 0.05, 0.02)
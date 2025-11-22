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

INFO_TEXT = [
    "If you lose in normal mode you might lose most weapons — Reavers Pike is rare; keep it safe. It never leaves your inventory.",
    "You can sell bad items to the trader and receive half the price.",
    "Green is common, blue is uncommon, magenta is rare and red are legendary.",
    "Buy the Eeavers Pike, and never lose it.",
    "One achievement requires you to use the trident",
    "Get five items and you will get an achievement",
    "There is a secret game mode, only the developers know of.",
    "The escalibur is very powerful, deals 20 damage, but is very unlikely to hit.",
    "The Eeavers Pike is half as common as the escalibur.",
    "The axe has a 95% chance to hit.",
    "You can always retreat if you play on easy mode.",
    "The costs and earnings after every battle is carefully calculated based on how powerful the item is.",
    "Even if you lose, you are lucky to get 5 loses, which gives you an award!",
    "Win five times to get an award!",
    "The name of every enemy is generated randomly.",
    "This game was a school project.",
    "Hard is very difficult indeed...",
    "The creator is from Sweden.",
    "Buy an item for ten times of what it gives you after winning a battle.",
    "Higher rarity doesn't necessarily mean it is better!",
    "The AI can be aggressive or protective.",
    "Keep at least one bleed weapon — bleed damage ticks are reliable over long fights.",
    "Selling a weapon returns half its shop value — sell low-value items to afford big upgrades.",
    "If you find a Reavers Pike, keep it. The final ending checks for it.",
    "Short Sword and Dagger are great early because bleed + high hit chance = steady wins.",
    "War Hammer hits hard but lowers scenery — use sparingly if you want second-chance chances.",
    "Escape carefully: retreating may randomly remove a weapon if you have more than one.",
    "Try to balance wins and losses — the final ending actually requires some losses.",
    "Rare and legendary give bigger rewards, but lower scenery or hit chance can hurt you.",
    "Use the trader to convert excess weapons into Makaronies — trader gives half the item value.",
    "High hit chance weapons (Axe, Dagger) are the fastest way to farm currency early.",
    "If you’re two-shotting enemies, switch to bleed weapons to finish prolonged fights faster.",
    "Experimental mode unlocks all items — not intended for normal progression.",
    "The game favors sustained DPS + scenery for long runs — abuse that synergy for finals.",
    "Keep three or more weapons to qualify for the final.",
    "Aim for both lifetime and current Makaronies — both matter for the final score.",
    "One achievement requires using the Trident — try it once!",
    "If you see 'Experimental' difficulty, expect all items unlocked."
]

RANDOM_SEED = None
STATE_CHANGE = (1.0, 0.15, 0.05, 0.02)
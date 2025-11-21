from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Achievement:
    name: str
    description: str

    @property
    def text(self) -> str:
        lines = self.description.split("\n")
        return f"{self.name} - {"\n".join(list(line if i == 0 else " "*(len(self.name)+3) for i, line in enumerate(lines)))}"

ACHIEVEMENTS = {
    "First Game": Achievement("First Game", "Everything starts at your first game"),
    "The Power Of The Trident": Achievement("The Power Of The Trident", "Use the trident for your first time, \nfeel the energy course through your body!")
}
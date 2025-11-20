from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Achievement:
    name: str
    description: str
    requirements: Dict[str, Any]

    @property
    def text(self) -> str:
        lines = self.description.split("\n")
        return f"{self.name} - {(line if i == 0 else " "*(len(self.name)+3) for i, line in enumerate(lines))}"

ACHIEVEMENTS = [
    Achievement("First Game", "Starts your first game.", {"Round": 1})
]
from typing import TYPE_CHECKING
from .core import (
    Translator,
    Structure,
    Language,
    Transcriber
)
if TYPE_CHECKING:
    __all__ = (
        "Translator",
        "Structure",
        "Language",
        "Transcriber"
    )
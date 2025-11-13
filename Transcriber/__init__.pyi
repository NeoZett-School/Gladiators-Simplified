from typing import Type, Callable
from ._internal import (
    Translator,
    Structure,
    Language,
    Transcriber
)

def new(basepath: str, extention: str, lang: Language) -> Transcriber: ...

class Module:
    Translator: Type[Translator]
    Structure: Type[Structure]
    Language: Type[Language]
    Transcriber: Type[Transcriber]
    Module: Type[Module]
    This: Module

    new: Callable

This: Module

__all__ = (
    "Translator",
    "Structure",
    "Language",
    "Transcriber",
    "Module",
    "This",
    "new"
)
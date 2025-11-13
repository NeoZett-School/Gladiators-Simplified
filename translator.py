from typing import Iterable, Optional, Generator, Any
from enum import Enum
import Transcriber as _Transcriber

from constants import LANGUAGE

class LanguageEnumMeta(type(Enum)): # So we create a metaclass for the language enum.
    def __contains__(cls, item: str) -> bool:
        item = str(item).lower().strip()
        return any(
            item in (lang.name.lower(), lang.value.prefix.lower(), lang.value.name.lower())
            for lang in cls
        )

    def __iter__(cls) -> Iterable:
        return iter(cls.__members__.values())

class Language(Enum, metaclass=LanguageEnumMeta): # We define languages
    SV = _Transcriber.Language("sv", "Swedish", "sv")
    EN = _Transcriber.Language("en", "English", "en")

    @property
    def value(self) -> _Transcriber.Language: # Redefine the value as an language
        return super().value

    @classmethod
    def get(cls, identifier: str) -> Optional["Language"]:
        identifier = identifier.lower().strip()
        for key, member in cls.__members__.items():
            lang = member.value
            if identifier in (key, lang.prefix, lang.name):
                return member
    
    @classmethod
    def iterate(cls) -> Generator["Language", Any, None]: # When we iterate over the members, we want to yield directly from the members for performance.
        yield from cls.__members__.values()

class Transcriber(_Transcriber.Transcriber):
    def __init__(self, lang: Language) -> None: # We'll only change the initialization behaviour.
        super().__init__(LANGUAGE.BASE_PATH, LANGUAGE.EXTENTION, lang.value) # We only take one language that we apply with constants.
from typing import Iterable, Optional, Generator, Any
from enum import Enum
import Transcriber as _Transcriber

class LanguageEnumMeta(type(Enum)):
    def __contains__(cls, item: str) -> bool:
        item = str(item).lower().strip()
        return any(
            item in (lang.name.lower(), lang.value.prefix.lower(), lang.value.name.lower())
            for lang in cls
        )

    def __iter__(cls) -> Iterable:
        return iter(cls.__members__.values())

class Language(Enum, metaclass=LanguageEnumMeta):
    SV = _Transcriber.Language("sv", "Swedish", "sv")
    EN = _Transcriber.Language("en", "English", "en")

    @property
    def value(self) -> _Transcriber.Language:
        return super().value

    @classmethod
    def get(cls, identifier: str) -> Optional["Language"]:
        identifier = identifier.lower().strip()
        for key, member in cls.__members__.items():
            lang = member.value
            if identifier in (key, lang.prefix, lang.name):
                return member
    
    @classmethod
    def iterate(cls) -> Generator["Language", Any, None]:
        yield from cls.__members__.values()

class Transcriber(_Transcriber.Transcriber):
    def __init__(self, lang: Language) -> None:
        super().__init__("./languages", ".lng", lang.value)
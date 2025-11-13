from typing import Set, Tuple, List, Dict, Union, Optional
from io import TextIOWrapper
import logging
import os
import re

IndexRange = Union[int, Tuple[int, Optional[int]]]

class Translator:
    """Automatically translate and replace simple sentences"""

    __associations: Dict[str, str]
    __slots__ = ("_Translator__associations",)

    def __init__(self, associations: Optional[Dict[str, str]] = None):
        self.__associations = associations if associations is not None else {}
    
    def translate(self, text: str) -> str:
        for k, v in self.__associations.items():
            text = re.sub(rf'\b{k}\b', v, text)
        return text

class Structure:
    """
    If every language are in the same file, 
    you may get the text of your language by knowing where 
    it is relative to the others.

    This is only practical once you have multiple languages 
    in one file.
    """

    __transcriber: "Transcriber"
    __lang: "Language"
    __start: int

    __slots__ = ("_Structure__transcriber", "_Structure__lang", "_Structure__start",)

    def __init__(self, transcriber: "Transcriber", lang: "Language", start: int) -> None:
        self.__transcriber = transcriber
        self.__lang = lang
        self.__start = start
    
    @property
    def transcriber(self) -> "Transcriber":
        return self.__transcriber
    
    @property
    def lang(self) -> "Language":
        return self.__lang

    def translate_index(self, i: int) -> int:
        return self.__start + i
    
    def get_index(self, index_range: IndexRange, end: Optional[int] = None) -> str:
        # Ensure transcriber language is correct
        if self.transcriber.lang != self.__lang:
            self.transcriber.set_lang(self.__lang)

        # Normalize index_range into a tuple
        if isinstance(index_range, int):
            if end is None:
                raise ValueError("end must be provided when index_range is an int")
            index_range = (index_range, end)
        elif end is not None:
            index_range = (index_range[0], end)

        # Translate indices
        translated = tuple(map(self.translate_index, index_range))

        # Get transcribed index string
        return self.__transcriber.get_index(translated)

class Language:
    """
    Define a language. 
    """

    translator: Translator

    __prefix: str
    __name: str
    __filename: str
    __frozen: bool
    __transcriptions: Set["Transcription"]
    __slots__ = ("translator", "_Language__prefix", "_Language__name", "_Language__filename", "_Language__transcriptions", "_Language__frozen",)

    def __init__(self, prefix: str, name: str, filename: str, translation: Optional[Translator] = None) -> None:
        self.__prefix = prefix
        self.__name = name
        self.__filename = filename
        self.__frozen = True
        self.translator = translation or Translator()

        self.__transcriptions = set()
    
    @property
    def transcriptions(self):
        return self.__transcriptions
    
    @transcriptions.setter
    def transcriptions(self, value: Set["Transcription"]):
        if not self.__frozen:
            self.__transcriptions = value
    
    @property
    def prefix(self) -> str:
        return self.__prefix
    
    @prefix.setter
    def prefix(self, value: str) -> None:
        if not self.__frozen:
            self.__prefix = value
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        if not self.__frozen:
            self.__name = value
    
    @property
    def filename(self) -> str:
        return self.__filename
    
    @filename.setter
    def filename(self, value: str) -> None:
        if not self.__frozen:
            self.__filename = value
    
    @property
    def frozen(self) -> bool:
        return self.__frozen
    
    @frozen.setter
    def frozen(self, value: bool) -> None:
        self.__frozen = value
    
    def translate(self, text: str) -> str:
        return self.translator.translate(text)
    
    def __hash__(self) -> int:
        return hash(self.__name)
    
    def __eq__(self, other):
        if not isinstance(other, Language):
            return NotImplemented
        return self.__name == other.__name

class Transcription:
    """
    Represents one transcription (either a single line or a range of lines).

    Language-specific text is stored keyed by a short language identifier (lang_key),
    e.g. Language.prefix or Language.filename. This avoids using Language objects
    as dict keys and avoids a reference cycle.
    """
    __transcriber: "Transcriber"
    __index_range: IndexRange
    __text: Dict[str, str]
    __loaded_for: Set[str]
    __slots__ = ("_Transcription__transcriber", "_Transcription__index_range", "_Transcription__text", "_Transcription__loaded_for", "__weakrefs__",)

    def __init__(self, index: IndexRange, transcriber: "Transcriber"):
        self.__transcriber = transcriber
        self.__index_range = index
        self.__text = {}
        self.__loaded_for = set()
    
    @staticmethod
    def _lang_key(lang: Language) -> str:
        # choose a stable, unique, small identifier for the language
        # `prefix` is typically short; `filename` is another option.
        return lang.prefix
    
    def load(self, lang: Language, lines: List[str]) -> None:
        """
        Load text for the given language from a list of lines.
        Stores a single string in self.__text[lang].
        """
        lang_key = self._lang_key(lang)

        if hasattr(lang, "transcriptions") and not self in lang.transcriptions:
            lang.transcriptions.add(self)
        if isinstance(self.__index_range, int):
            try:
                text = lines[self.__index_range]
            except IndexError:
                raise IndexError(f"Line index {self.__index_range} out of range (0..{len(lines)-1})")
        else:
            start, end = self.__index_range
            if end is None:
                end = start + 1
            selected = lines[start:end]
            text = "".join(selected)
        self.__text[lang_key] = self.__transcriber.lang.translate(text.rstrip("\n"))
        self.__loaded_for.add(lang_key)
    
    def evict_lang(self, lang_key: str) -> None:
        self.__loaded_for.remove(lang_key)
    
    @property
    def loaded_for(self) -> Set[str]:
        return self.__loaded_for
    
    @property
    def index_range(self) -> IndexRange:
        return self.__index_range

    @property
    def text(self) -> str:
        """Return text for the transcriber's current language."""
        lang_key = self._lang_key(self.__transcriber.lang)
        try:
            return self.__text[lang_key]
        except KeyError as exc:
            raise KeyError(f"Transcription not loaded for language '{lang_key}'. Call get_index(...) first.") from exc
    
    def __hash__(self) -> int:
        return hash(self.__index_range)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Transcription):
            return NotImplemented
        return self.__index_range == other.__index_range

class Cache:
    transcriber: "Transcriber"
    transcriptions: Dict[IndexRange, Transcription]
    lines: List[str]

    __read: bool
    __slots__ = ("transcriber", "transcriptions", "lines", "_Cache__read", "__weakrefs__",)

    def __init__(self, transcriber: "Transcriber") -> None:
        self.transcriber = transcriber
        self.transcriptions = {}
        self.lines = []
        self.__read = False
    
    def reset_all(self) -> None:
        """Clear everything (used when resetting)."""
        self.transcriptions.clear()
        self.lines.clear()
        self.__read = False
    
    def reset(self) -> None:
        """Clear lines and read flag but keep cached Transcription objects (used when changing language)."""
        self.lines.clear()
        self.__read = False
    
    def get_index(self, index_range: IndexRange) -> str:
        if not self.__read:
            raise RuntimeError("Transcription file not read; call Cache.read(file) first.")
        if not index_range in self.transcriptions:
            inst = Transcription(index_range, self.transcriber)
            inst.load(self.transcriber.lang, self.lines)
            self.transcriptions[index_range] = inst
            return inst.text
        inst = self.transcriptions[index_range]
        lang_key = Transcription._lang_key(self.transcriber.lang)
        if not lang_key in inst.loaded_for:
            inst.load(self.transcriber.lang, self.lines)
        return inst.text
    
    def read(self, file: TextIOWrapper) -> None:
        self.lines = file.readlines()
        self.__read = True

class Transcriber:
    basepath: str
    extension: str

    __lang: Language
    __cache: Cache

    __slots__ = ("basepath", "extension", "_Transcriber__lang", "_Transcriber__cache", "__weakrefs__",)

    def __init__(self, basepath: str, extension: str, lang: Language) -> None:
        self.basepath = basepath
        self.extension = extension
        self.__lang = lang
        self.__cache = Cache(self)
        self.load()
        logging.info("Transcriber is ready.")
    
    @property
    def path(self) -> str:
        return os.path.join(self.basepath, self.lang.filename+self.extension)
    
    @property
    def lang(self) -> Language:
        return self.__lang
    
    @lang.setter
    def lang(self, value: Language) -> None:
        self.set_lang(value)
    
    def reset(self) -> None:
        """Reset everything (clear loaded transcriptions and cached lines)."""
        self.__cache.reset_all()
    
    def set_lang(self, lang: Language) -> None:
        self.__cache.reset()
        self.__lang = lang
        self.load()
    
    def load(self, encoding: str = "utf-8") -> None:
        try:
            with open(self.path, "r", encoding=encoding) as f:
                self.__cache.read(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Transcription file not found at {self.path}") from e

    def get_index(self, index_range: IndexRange, end: Optional[int] = None) -> str:
        # Case 1: two integer arguments — combine into a tuple
        if end is not None:
            if isinstance(index_range, int):
                index_range = (index_range, end)
            else:
                index_range = (index_range[0], end)
        return self.__cache.get_index(index_range)
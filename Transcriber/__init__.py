"""
The `Transcriber` package provides features for transcribing 
text. Wheter you want to use it for a game or an application, 
you can depend on dedicated transcriptions.

Copyright (C) 2025-2026 Neo Zetterberg
"""

from typing import Type, Any
from ._internal import (
    Translator,
    Structure,
    Language,
    Transcriber
)
import sys

#####################################################
# Module lets the user access any items as defined. #
# It also lets us create a much more comprehensive  #
#  structure and lets us use `__init__` f.e.        #
# ------------------------------------------------- #
# You may still import like normal:                 #
# from Transcriber import This         | Works      #
# import Transcriber                   |            #
# print(Transcriber.This)              | Works      #
# import Transcriber as T              |            #
# print(T.This)                        | Also works #
#####################################################

class Module:
    def __class_getitem__(cls, item: Any) -> None:
        raise PermissionError("You are not allowed to use this method.")
    def __init_subclass__(cls) -> None:
        raise PermissionError("You are not allowed to use this method.")
    def __get__(self, instance: Any, owner: Type) -> Any:
        raise PermissionError("You are not allowed to use this method.")
    def __set__(self, instance: Any, value: Any) -> None:
        raise PermissionError("You are not allowed to use this method.")
    def __getattribute__(self, name: str) -> Any:
        match name:
            case "Translator":
                return Translator
            case "Structure":
                return Structure
            case "Language":
                return Language
            case "Transcriber":
                return Transcriber
            case "Module":
                return Module
            case "This":
                return self
            case "new":
                return lambda basepath, extention, lang: Transcriber(basepath, extention, lang)
    def __setattr__(self, name: str, value: Any) -> None:
        raise PermissionError("You are not allowed to change any attribute of this package.")
    def __getitem__(self, key: Any) -> None:
        raise PermissionError("You are not allowed to use this method.")
    def __setitem__(self, key: Any, value: Any) -> None:
        raise PermissionError("You are not allowed to use this method.")

sys.modules[__name__] = Module()
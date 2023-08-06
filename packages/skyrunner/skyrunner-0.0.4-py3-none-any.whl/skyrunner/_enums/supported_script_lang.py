from enum import Enum

from .enum_meta import EnumMeta


class SupportedScriptLang(Enum, metaclass=EnumMeta):
    PYTHON = 'python'


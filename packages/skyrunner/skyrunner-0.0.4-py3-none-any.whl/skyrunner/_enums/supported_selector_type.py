from enum import Enum

from .enum_meta import EnumMeta


class SupportedSelectorType(Enum, metaclass=EnumMeta):
    XPATH = 'xpath'
    ID = 'id'

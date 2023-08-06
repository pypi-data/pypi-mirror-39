from enum import Enum

from .enum_meta import EnumMeta


class SupportedBrowser(Enum, metaclass=EnumMeta):
    CHROME = 'chrome'
    FIREFOX = 'firefox'

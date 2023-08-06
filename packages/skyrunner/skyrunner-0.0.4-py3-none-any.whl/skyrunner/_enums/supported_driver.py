from enum import Enum

from .enum_meta import EnumMeta


class SupportedDriver(Enum, metaclass=EnumMeta):
    WEBDRIVER = 'webdriver'


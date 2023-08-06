from enum import Enum

from .enum_meta import EnumMeta


class SupportedActions(Enum, metaclass=EnumMeta):
    LINK = 'link'
    INPUT = 'input'
    SHARED_INPUT = 'shared_input'
    ENTER = 'enter'
    CLICK = 'click'
    CUSTOM = 'custom'

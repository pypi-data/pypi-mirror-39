from enum import EnumMeta


class EnumMeta(EnumMeta):
    def list(self):
        return list(map(lambda e: e.value, self))

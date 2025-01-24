from enum import Enum


class MatchTypeEnum(str, Enum):
    MATCH_1 = "1"
    MATCH_2 = "2"

    def __repr__(self):
        return str(self.value)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, int):
            return cls(str(value))

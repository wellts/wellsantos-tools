from enum import Enum


class StringEnum(str, Enum):
    def __str__(self):
        return self.value

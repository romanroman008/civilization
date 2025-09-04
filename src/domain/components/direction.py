

from enum import Enum
from functools import lru_cache
from typing import Optional

from domain.components.position import Position


class Direction(Enum):
    TOP = ((0, -1), 180)
    BOT = ((0, 1), 0)
    LEFT = ((-1, 0), 90)
    RIGHT = ((1, 0), -90)

    def vector(self) -> Position:
        return Position(*self.value[0])

    @property
    def angle(self):
        return self.value[1]

    @classmethod
    def min_rotation_degrees(cls):
        return 90

    @classmethod
    @lru_cache(maxsize=1)
    def _vector_to_direction(cls):
        return {d.value[0]: d for d in cls}

    @classmethod
    def to_direction(cls, delta:tuple[int, int]) -> Optional["Direction"]:
        dx, dy = delta

        ndx = (dx > 0) - (dx < 0)
        ndy = (dy > 0) - (dy < 0)
        return cls._vector_to_direction().get((ndx, ndy))


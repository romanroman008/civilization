

from enum import Enum
from functools import lru_cache
from typing import Optional, Union



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

    @staticmethod
    def _normalize(dx: int, dy: int) -> tuple[int, int]:
        ndx = (dx > 0) - (dx < 0)
        ndy = (dy > 0) - (dy < 0)
        return ndx, ndy

    @classmethod
    def to_direction(cls, delta:tuple[int, int]) -> Optional["Direction"]:
        dx, dy = delta

        ndx = (dx > 0) - (dx < 0)
        ndy = (dy > 0) - (dy < 0)
        return cls._vector_to_direction().get((ndx, ndy))

    @classmethod
    def reverse_direction(cls, direction: Union["Direction", tuple[int,int], Position]) -> Optional["Direction"]:
        if isinstance(direction, Direction):
            dx, dy = direction.value[0]
            ndx, ndy = -dx, -dy

        elif isinstance(direction, Position):
            dx, dy = direction
            ndx, ndy = cls._normalize(-dx, -dy)

        else:
            dx,dy = direction
            ndx, ndy = cls._normalize(-dx, -dy)

        if ndx == 0 and ndy == 0:
            return None

        return cls._vector_to_direction().get((ndx, ndy))





from enum import Enum

from domain.components.position import Position


class Direction(Enum):
    TOP = ((0, -1), 180)
    BOT = ((0, 1), 0)
    LEFT = ((-1, 0), 90)
    RIGHT = ((1, 0), 270)
    IDLE = ((0, 0), 0)

    def vector(self):
        return Position(*self.value[0])

    @property
    def angle(self):
        return self.value[1]
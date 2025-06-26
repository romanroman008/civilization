from enum import Enum

from domain.world.entieties.position import Position


class Direction(Enum):
    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)
    IDLE = (0, 0)

    def vector(self):
        return Position(*self.value)
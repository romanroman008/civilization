from typing import Tuple

from domain.components.direction import Direction
from domain.organism.movement.action.rotation_action import RotationAction


def normalize_angle(angle) -> float:
    r = (angle + 180) % 360 - 180
    return 180 if r == -180 else r

ROTATION_TO_DIRECTION = {
    0.0: Direction.BOT,
    90.0: Direction.LEFT,
    180.0: Direction.TOP,
    -90.0: Direction.RIGHT,
}

class Transform:
    def __init__(self, x: float, y: float, rotation: float):
        self._x: float = x
        self._y: float = y
        self._rotation: float = normalize_angle(rotation)
        self._direction: Direction = Direction.BOT
        self._set_proper_direction()

    def interpolate_x(self, x:float):
        self._x += x

    def interpolate_y(self, y:float):
        self._y += y

    def rotate(self, value: float):
        self._rotation = normalize_angle(self._rotation + value)
        self._set_proper_direction()

    def translated_xy(self, direction: Direction) -> Tuple[float, float]:
        return self._x + direction.vector().x, self._y + direction.vector().y

    def _set_proper_direction(self):
        self._direction = ROTATION_TO_DIRECTION.get(self._rotation, self._direction)


    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def rotation(self):
        return self._rotation

    @property
    def direction(self) -> Direction:
        return self._direction


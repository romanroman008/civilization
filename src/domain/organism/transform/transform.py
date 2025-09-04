from typing import Tuple, Callable

from domain.components.direction import Direction
from domain.components.position import Position


from shared.constans import OFFSET_TO_POSITION_RATIO





def normalize_angle(angle) -> int:
    r = (angle + 180) % 360 - 180
    return 180 if r == -180 else r

ROTATION_TO_DIRECTION = {
    0.0: Direction.BOT,
    90.0: Direction.LEFT,
    180.0: Direction.TOP,
    -90.0: Direction.RIGHT,
}



class Transform:
    __slots__ = ("_x", "_y", "_offset_x", "_offset_y",
                 "_rotation", "_direction",
                 "_readonly", "_writer", "_on_arrival")
    def __init__(self, x: int, y: int, rotation: float):
        self._x: int = x
        self._y: int = y
        self._offset_x: int = 0
        self._offset_y: int = 0
        self._rotation: int = normalize_angle(rotation)
        self._direction: Direction = ROTATION_TO_DIRECTION.get(self._rotation, Direction.BOT)

        self._readonly: TransformReadOnly = TransformReadOnly(self)
        self._writer: TransformWriter = TransformWriter(self)

        self._on_arrival: Callable[[Position], None] | None = None


    def set_change_position_callback(self, callback):
        if self._on_arrival:
            raise RuntimeError("Arrival callback already set")
        self._on_arrival = callback

    def finalize_move(self, target_position: Position):
        self._on_arrival(target_position)

    def interpolate_x(self, offset_x:int):
        total_offset = self._offset_x + offset_x
        ratio = OFFSET_TO_POSITION_RATIO
        delta = total_offset // ratio if total_offset >= 0 else -((-total_offset) // ratio)
        if delta == 0:
            self._offset_x = total_offset
            return
        self._x += delta
        self._offset_x = total_offset - delta * ratio

    def interpolate_y(self, offset_y:int):
        total_offset = self._offset_y + offset_y
        ratio = OFFSET_TO_POSITION_RATIO
        delta = total_offset // ratio if total_offset >= 0 else -((-total_offset) // ratio)
        if delta == 0:
            self._offset_y = total_offset
            return
        self._y += delta
        self._offset_y = total_offset - delta * ratio

    def rotate(self, value: int) -> None:
        r = self._rotation + value
        r %= 360
        self._rotation = r - 360 if r > 180 else r
        self._direction = ROTATION_TO_DIRECTION.get(self._rotation, self._direction)

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
    def offset_x(self):
        return self._offset_x

    @property
    def offset_y(self):
        return self._offset_y

    @property
    def rotation(self):
        return self._rotation

    @property
    def direction(self) -> "Direction":
        return self._direction

    @property
    def position(self) -> "Position":
        return Position(self._x, self._y)

    @property
    def readonly(self) -> "TransformReadOnly":
        return self._readonly

    @property
    def writer(self) -> "TransformWriter":
        return self._writer

class TransformReadOnly:
    __slots__ = ("_transform",)

    def __init__(self, transform: "Transform"):
        object.__setattr__(self, "_transform", transform)

    @property
    def x(self) -> int: return self._transform.x

    @property
    def y(self) -> int: return self._transform.y

    @property
    def offset_x(self) -> int: return self._transform.offset_x

    @property
    def offset_y(self) -> float: return self._transform.offset_y

    @property
    def rotation(self) -> int: return self._transform.rotation

    @property
    def direction(self) -> "Direction": return self._transform.direction

    @property
    def position(self) -> "Position": return self._transform.position

    def translated_xy(self, direction: "Direction") -> tuple[float, float]:
        return self._transform.translated_xy(direction)

    def __setattr__(self, *_a, **_k):
        raise AttributeError("TransformReadOnly is read-only")



class TransformWriter:
    __slots__ = ("_transform",)

    def __init__(self, transform: "Transform"):
        self._transform = transform

    def interpolate_x(self, delta_x: int) -> None: self._transform.interpolate_x(delta_x)

    def reset_offset_x(self) -> None: self._transform._offset_x = 0

    def reset_offset_y(self) -> None:self._transform._offset_y = 0

    def match_rotation_to_direction(self) -> None: self._transform._rotation = self._transform.direction.angle

    def interpolate_y(self, delta_y: int) -> None: self._transform.interpolate_y(delta_y)

    def rotate(self, delta_degrees: int) -> None:  self._transform.rotate(delta_degrees)

    def finalize_move(self, target_position: Position) -> None: self._transform.finalize_move(target_position)



from typing import Tuple, Callable

from domain.components.direction import Direction
from domain.components.position import Position
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.organism.transform.transform_readonly import TransformReadOnly
    from domain.organism.transform.transform_writer import TransformWriter


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
    def direction(self) -> "Direction":
        return self._direction

    @property
    def position(self) -> "Position":
        return Position(round(self._x), round(self._y))

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
    def x(self) -> float: return self._transform.x
    @property
    def y(self) -> float: return self._transform.y
    @property
    def rotation(self) -> float: return self._transform.rotation
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

    def interpolate_x(self, delta_x: float) -> None: self._transform.interpolate_x(delta_x)

    def interpolate_y(self, delta_y: float) -> None: self._transform.interpolate_y(delta_y)

    def rotate(self, delta_degrees: float) -> None:  self._transform.rotate(delta_degrees)

    def finalize_move(self, target_position: Position) -> None: self._transform.finalize_move(target_position)

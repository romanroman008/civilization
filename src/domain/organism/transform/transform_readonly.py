from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.transform.transform import Transform


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
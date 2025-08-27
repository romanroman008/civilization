from domain.components.position import Position
from domain.organism.transform.transform import Transform


class TransformWriter:
    __slots__ = ("_transform",)

    def __init__(self, transform: "Transform"):
        self._transform = transform

    def interpolate_x(self, delta_x: float) -> None: self._transform.interpolate_x(delta_x)

    def interpolate_y(self, delta_y: float) -> None: self._transform.interpolate_y(delta_y)

    def rotate(self, delta_degrees: float) -> None:  self._transform.rotate(delta_degrees)

    def finalize_move(self, target_position: Position) -> None: self._transform.finalize_move(target_position)
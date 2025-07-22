from typing import Protocol


from domain.components.position import Position


class Renderable(Protocol):
    @property
    def sprite_key(self) -> str: ...

    @property
    def position(self) -> Position: ...

    @property
    def rotation(self) -> float: ...

    @property
    def offset(self) -> tuple[float, float]: ...







from typing import Protocol

from domain.world.entieties.position import Position


class Renderable(Protocol):
    @property
    def sprite_key(self) -> str: ...

    @property
    def position(self) -> Position: ...
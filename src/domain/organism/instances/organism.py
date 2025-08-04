from typing import Protocol, runtime_checkable
from domain.components.position import Position
from domain.organism.organism_id import OrganismID



@runtime_checkable
class Organism(Protocol):
    @property
    def id(self) -> OrganismID: ...

    @property
    def sprite_key(self) -> str: ...

    @property
    def allowed_terrains(self): ...

    @property
    def position(self) -> Position: ...

    @property
    def rotation(self) -> int: ...

    @property
    def offset(self) -> tuple[int, int]: ...

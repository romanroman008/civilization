from abc import ABC, abstractmethod
from typing import TypeVar

from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.organism_id import OrganismID

from domain.organism.transform.transform import Transform

P = TypeVar("P", bound="OrganismPrefab")

class Organism(ABC):
    def __init__(self, prefab: P, position: Position, transform: Transform):
        self._prefab = prefab
        self._position = position
        self._transform = transform


    @property
    @abstractmethod
    def id(self) -> OrganismID: ...

    @property
    def sprite_key(self) -> str:
        return self._prefab.name

    @property
    def allowed_terrains(self) -> set[Terrain]:
        return self._prefab.allowed_terrains

    @property
    def position(self) -> Position:
        return self._position

    @property
    def rotation(self) -> float:
        return self._transform.rotation

    @property
    def x(self) -> float:
        return self._transform.x

    @property
    def y(self) -> float:
        return self._transform.y

    @property
    @abstractmethod
    def is_alive(self) -> bool: ...

    @abstractmethod
    def tick(self): pass










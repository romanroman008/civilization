from abc import ABC, abstractmethod

from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.organism_id import OrganismID
from domain.organism.prefabs.organism_prefab import OrganismPrefab



class Organism(ABC):
    def __init__(self, prefab: OrganismPrefab, position: Position):
        self._prefab = prefab
        self._position = position
        self._rotation = 0
        self._offset_x = 0
        self._offset_y = 0


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
    def rotation(self) -> int:
        return self._rotation

    @property
    def offset(self) -> tuple[int,int]:
        return self._offset_x, self._offset_y

    @property
    @abstractmethod
    def is_alive(self) -> bool: ...








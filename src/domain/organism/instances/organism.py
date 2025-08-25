from abc import ABC, abstractmethod

from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.organism_id import OrganismID
from domain.organism.prefabs.organism_prefab import OrganismPrefab



class Organism(ABC):
    def __init__(self, prefab: OrganismPrefab, position: Position):
        self._prefab = prefab
        self._position = position



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
    @abstractmethod
    def rotation(self) -> int: pass

    @property
    @abstractmethod
    def x(self) -> float: pass

    @property
    @abstractmethod
    def y(self) -> float: pass


    @property
    def offset(self) -> tuple[int,int]:
        return self._offset_x, self._offset_y

    @property
    @abstractmethod
    def is_alive(self) -> bool: ...

    def tick(self): pass








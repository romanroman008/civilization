from abc import ABC
from itertools import count

from domain.components.position import Position
from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Organism(ABC):
    _id_counter = count(1)
    def __init__(self, prefab: OrganismPrefab, position: Position):
        self._id = next(Organism._id_counter)
        self._prefab = prefab
        self._position = position
        self._rotation = 0
        self._offset = (0,0)


    def __call__(self, *args, **kwargs):
        pass

    @property
    def id(self) -> int:
        return self._id

    @property
    def sprite_key(self) -> str:
        return self._prefab.name

    @property
    def allowed_terrains(self):
        return self._prefab.allowed_terrains

    @property
    def position(self) -> Position:
        return self._position

    @property
    def rotation(self) -> int:
        return self._rotation

    @property
    def offset(self) -> tuple[int, int]:
        return self._offset



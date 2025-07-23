from abc import ABC

from domain.components.position import Position
from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Organism(ABC):
    def __init__(self, prefab: OrganismPrefab, position: Position):
        self._prefab = prefab
        self._position = position
        self._rotation = 0
        self._offset = (0,0)


    def __call__(self, *args, **kwargs):
        pass

    @property
    def sprite_key(self) -> str:
        return self._prefab.name

    @property
    def block_radius(self) -> int:
        return self._prefab.block_radius

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



from itertools import count

from domain.components.position import Position
from domain.organism.instances.organism import Organism
from domain.organism.prefabs.plant_prefab import PlantPrefab


class Plant(Organism):
    _id_counter = count(1)

    def __init__(self, prefab: PlantPrefab, position: Position):
        self._id = next(Plant._id_counter)
        self._prefab: PlantPrefab = prefab
        self._position: Position = position
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

    @property
    def is_edible(self):
        return self._prefab.is_edible
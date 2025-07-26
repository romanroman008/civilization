from domain.components.position import Position
from domain.organism.instances.organism import Organism
from domain.organism.prefabs.plant_prefab import PlantPrefab


class Plant(Organism):

    def __init__(self, prefab: PlantPrefab, position: Position):
        super().__init__(prefab, position)
        self._prefab: PlantPrefab = prefab

    def __call__(self, *args, **kwargs):
        pass


    @property
    def is_edible(self):
        return self._prefab.is_edible
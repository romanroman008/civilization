from itertools import count

from domain.components.position import Position
from domain.organism.instances.organism import Organism

from domain.organism.organism_id import OrganismID
from domain.organism.prefabs.plant_prefab import PlantPrefab
from domain.organism.transform.transform import Transform
from domain.services.event_bus import EventBus


class Plant(Organism):
    _id_counter = count(1)

    def __init__(self,
                 prefab: PlantPrefab,
                 position: Position,
                 transform: Transform,
                 event_bus: EventBus
                 ):
        super().__init__(prefab, position, transform)
        self._id = OrganismID("plant", next(self._id_counter))
        self._event_bus = event_bus
        self._is_alive = True


    @property
    def id(self) -> OrganismID:
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
    def is_edible(self):
        return self._prefab.is_edible

    @property
    def is_alive(self) -> bool:
        return self._is_alive


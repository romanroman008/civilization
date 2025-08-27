from domain.components.position import Position
from domain.organism.instances.plant import Plant
from domain.organism.prefabs.plant_prefab import PlantPrefab
from domain.organism.transform.transform import Transform

from domain.services.event_bus import EventBus


class PlantFactory:
    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    def create(self, prefab: PlantPrefab, position: Position) -> Plant:
        transform = Transform(position.x, position.y, prefab.initial_rotation)
        return Plant(prefab, position, transform, self._event_bus)
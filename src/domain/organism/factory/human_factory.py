from domain.components.position import Position
from domain.organism.brain.human_brain import HumanBrain
from domain.organism.factory.animal_factory import AnimalFactory
from domain.organism.instances.human import Human
from domain.organism.movement.human_movement import HumanMovement
from domain.organism.perception.field_of_view import FieldOfView
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.organism.transform.transform import Transform

from domain.organism.vitals import Vitals
from domain.services.event_bus import EventBus
from domain.world_map.vision_port import VisionPort


class HumanFactory:
    def __init__(self, vision_port: VisionPort, event_bus: EventBus):
        self._vision_port = vision_port
        self._event_bus = event_bus

    def create(self, prefab: OrganismPrefab, position: Position) -> Human:
        transform = Transform(position.x, position.y, prefab.initial_rotation)
        movement = HumanMovement(transform_writer=transform.writer, transform_readonly=transform.readonly)
        vitals = Vitals()
        field_of_view = FieldOfView(radius=5, vision_port=self._vision_port)
        brain = HumanBrain(field_of_view=field_of_view,
                           vitals=vitals,
                           movement=movement,
                           transform_readonly=transform.readonly,
                           event_bus=self._event_bus)
        return Human(prefab, position, brain, transform)
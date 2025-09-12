from domain.components.position import Position
from domain.organism.brain.brain import Brain
from domain.organism.brain.path_planner import PathPlanner
from domain.organism.instances.animal import Animal
from domain.organism.movement.animal_movement import AnimalMovement

from domain.organism.perception.vision import Vision
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.organism.transform.transform import Transform
from domain.organism.vitals import Vitals
from domain.services.event_bus import EventBus

from domain.world_map.vision_port_protocol import VisionPortProtocol
from shared.id_registry import IdRegistry


class AnimalFactory:
    def __init__(self, vision_port: VisionPortProtocol, id_registry: IdRegistry, event_bus: EventBus):
        self._vision_port = vision_port
        self._id_registry = id_registry
        self._event_bus = event_bus

    def create(self, prefab: OrganismPrefab, position: Position) -> Animal:
        transform = Transform(position.x, position.y ,prefab.initial_rotation)
        movement = AnimalMovement(transform.writer, transform.readonly)
        vitals = Vitals()
        vision = Vision(transform.readonly, self._vision_port, self._id_registry, prefab.allowed_terrains)
        path_planner = PathPlanner(vision,transform.readonly, prefab.allowed_terrains)
        brain = Brain(vision=vision,
                      vitals=vitals,
                      movement=movement,
                      transform_readonly=transform.readonly,
                      path_planner=path_planner,
                      event_bus=self._event_bus,
                      available_terrains=prefab.allowed_terrains)
        animal = Animal(prefab, position, brain, transform)
        brain.set_owner_id(animal.id)
        return animal






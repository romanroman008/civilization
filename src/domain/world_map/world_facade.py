from itertools import chain
from typing import Sequence, Iterable, Optional


from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.human.perception.animal_info import AnimalInfo
from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism

from domain.organism.organism_id import OrganismID
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult
from domain.world_map.world_interactions_handler import WorldInteractionsHandler
from domain.world_map.world_interactions_validator import WorldInteractionsValidator

from domain.world_map.world_map import WorldMap

from domain.world_map.world_state_service import WorldStateService

def _tile_to_perceived_object(relative_positon: Position, terrain: Terrain, organism:Optional[Organism]) -> PerceivedObject:
    if organism:
        organism_info = _organism_to_organism_info(relative_positon, organism)
        return PerceivedObject(relative_positon, terrain, organism_info)
    return PerceivedObject(relative_positon, terrain, None)

def _organism_to_organism_info(relative_position: Position, organism: Organism) -> OrganismInfo:
    if isinstance(organism, Animal):
        return AnimalInfo(organism.id, relative_position, organism.is_alive)
    return OrganismInfo(organism.id, relative_position, organism.is_alive)


class WorldFacade:
    def __init__(self, world_map: WorldMap,
                 world_state_service: WorldStateService,
                 event_bus: EventBus):
        self._world_map = world_map
        self._world_state_service = world_state_service
        self._event_bus = event_bus
        self._world_interactions_validator = self._create_world_interactions_validator()
        self._create_world_interactions_handler()

    @property
    def height(self) -> int:
        return self._world_map.height

    @property
    def width(self) -> int:
        return self._world_map.width

    @property
    def event_bus(self):
        return self._event_bus

    def _create_world_interactions_validator(self):
        return WorldInteractionsValidator(world_map=self._world_map,
                                          world_state_service=self._world_state_service)

    def _create_world_interactions_handler(self):
        return WorldInteractionsHandler(world_map=self._world_map,
                                        world_state_service=self._world_state_service,
                                        event_bus=self._event_bus,
                                        world_interactions_validator=self._world_interactions_validator)


    def add_organism(self, organism: Organism):
        self._world_state_service.register_organism(organism)

    def update_position(self, organism_id: OrganismID, new_position: Position):
        self._world_state_service.update_position(organism_id, new_position)

    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool:
        return self._world_interactions_validator.is_position_allowed(position, allowed_terrains)

    def reserve_position(self, position: Position):
        self._world_state_service.reserve_position(position)


    def get_visible_area(self, observer_position, positions: list[Position]) -> list[PerceivedObject]:
        perceived_objects = []
        for position in positions:
            terrain = self._world_map.get_terrain_at_position(position)
            if not terrain:
                continue
            organism = self._world_state_service.get_organism_at_position(position)
            relative_positon = position - observer_position
            perceived_object = _tile_to_perceived_object(relative_positon, terrain, organism)
            perceived_objects.append(perceived_object)
        return perceived_objects


    def get_all_renderable(self) -> Iterable[Renderable]:
        tiles = self._world_map.get_all_renderable()
        organisms = self._world_state_service.get_all_renderable()
        return chain(tiles,organisms)



    def get_example_agent(self) -> Optional[Human]:
        return self._world_state_service.get_example_agent()



from __future__ import annotations
import logging
from itertools import chain
from typing import Iterable, Optional

from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.organism.perception.animal_info import AnimalInfo
from domain.organism.perception.organism_info import OrganismInfo
from domain.organism.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism

from domain.services.event_bus import EventBus

from domain.world_map.world_interactions_handler import WorldInteractionsHandler
from domain.world_map.world_interactions_validator import WorldInteractionsValidator

from domain.world_map.world_map import WorldMap

from domain.world_map.world_state_service import WorldStateService
from infrastructure.rendering.world_snapshot_adapter import WorldSnapshotAdapter
from shared.logger import get_logger


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
        self._logger = get_logger("WorldFacade", level=logging.INFO,
                                  log_filename="world_interactions_handler.log")

        self._world_adapter = WorldSnapshotAdapter(world_state_service, world_map)
        self._vision_port = VisionPort(self)

    @property
    def height(self) -> int:
        return self._world_map.height

    @property
    def width(self) -> int:
        return self._world_map.width

    @property
    def event_bus(self):
        return self._event_bus

    @property
    def vision_port(self) -> "VisionPort":
        return self._vision_port

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


    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool:
        return self._world_interactions_validator.is_position_allowed(position, allowed_terrains)


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

    def tick(self):
        for organism in self._world_state_service.get_all_organisms():
            organism.tick()



class VisionPort:
    __slots__ = "_world_facade"
    def __init__(self, world_facade: "WorldFacade"):
        self._world_facade = world_facade


    def get_vision(self, observer_position, positions: list["Position"]) -> list["PerceivedObject"]:
        return self._world_facade.get_visible_area(observer_position, positions)





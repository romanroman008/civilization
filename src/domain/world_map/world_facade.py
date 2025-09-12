from __future__ import annotations
import logging
from itertools import chain
from typing import Iterable, Optional, Tuple


from domain.components.terrain import Terrain

from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism

from domain.organism.perception.world_perception_adapter_protocol import WorldPerceptionAdapterProtocol

from domain.services.event_bus import EventBus

from domain.world_map.vision_port_protocol import VisionPortProtocol

from domain.world_map.world_interactions_handler import WorldInteractionsHandler

from domain.world_map.world_interactions_validator_protocol import WorldInteractionsValidatorProtocol

from domain.world_map.world_map import WorldMap

from domain.world_map.world_state_service import WorldStateService
from infrastructure.rendering.world_snapshot_adapter import WorldSnapshotAdapter
from shared.id_registry import IdRegistry
from shared.logger import get_logger


class WorldFacade:
    def __init__(self, world_map: WorldMap,
                 world_state_service: WorldStateService,
                 vision_port_protocol: VisionPortProtocol,
                 world_perception_adapter_protocol: WorldPerceptionAdapterProtocol,
                 world_interactions_validator_protocol: WorldInteractionsValidatorProtocol,
                 id_registry: IdRegistry,
                 event_bus: EventBus):
        self._world_map = world_map
        self._world_state_service = world_state_service
        self._id_registry = id_registry
        self._event_bus = event_bus
        self._world_interactions_validator = world_interactions_validator_protocol
        self._create_world_interactions_handler()
        self._logger = get_logger("WorldFacade", level=logging.INFO,
                                  log_filename="world_interactions_handler.log")

        self._world_adapter = WorldSnapshotAdapter(world_state_service, world_map)
        self._vision_port = vision_port_protocol
        self._world_perception_adapter = world_perception_adapter_protocol

    @property
    def height(self) -> int:
        return self._world_map.height

    @property
    def width(self) -> int:
        return self._world_map.width

    @property
    def id_registry(self) -> IdRegistry:
        return self._id_registry

    @property
    def event_bus(self):
        return self._event_bus

    @property
    def vision_port(self) -> "VisionPortProtocol":
        return self._vision_port


    def _create_world_interactions_handler(self):
        return WorldInteractionsHandler(world_map=self._world_map,
                                        world_state_service=self._world_state_service,
                                        event_bus=self._event_bus,
                                        world_interactions_validator=self._world_interactions_validator)


    def add_organism(self, organism: Organism):
        self._world_state_service.register_organism(organism)


    def is_position_allowed(self, position: tuple[int,int], allowed_terrains: set[Terrain]) -> bool:
        return self._world_interactions_validator.is_position_allowed((position[0],position[1]), allowed_terrains)


    def get_organisms_at_positions(self, positions:list[Tuple[int,int]]):
        return self._world_state_service.get_organisms_at_positions(positions)







    def get_example_agent(self) -> Optional[Human]:
        return self._world_state_service.get_example_agent()

    def tick(self, tick:int):
        for organism in self._world_state_service.get_all_organisms():
            organism.tick(tick)








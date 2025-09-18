from typing import Sequence

import numpy as np
from tqdm import tqdm

from domain.organism.perception.world_perception_adapter import WorldPerceptionAdapter
from domain.organism.perception.world_perception_adapter_protocol import WorldPerceptionAdapterProtocol
from domain.services.event_bus import EventBus
from domain.services.generators.human_generator import HumanGenerator
from domain.world_map.tile import Tile
from domain.world_map.vision_port import VisionPort
from domain.world_map.world_facade import WorldFacade
from domain.world_map.world_interactions_validator import WorldInteractionsValidator
from domain.world_map.world_map import WorldMap
from domain.services.generators.animals_generator import AnimalsGenerator
from domain.services.generators.elevation_generator import ElevationGenerator
from domain.services.generators.plants_generator import PlantsGenerator
from domain.services.tile_adapter import TileAdapter

from domain.world_map.world_state_service import WorldStateService
from infrastructure.rendering.world_snapshot_adapter import WorldSnapshotAdapter
from shared.id_registry import IdRegistry






class WorldGenerator:

    def __init__(self,
                 logger,
                 elevation_generator: ElevationGenerator,
                 plants_generator: PlantsGenerator,
                 animals_generator: AnimalsGenerator,
                 human_generator: HumanGenerator,
                 event_bus: EventBus
                 ):

        self.logger = logger
        self.event_bus = event_bus

        self.elevation_generator = elevation_generator
        self.plants_generator = plants_generator
        self.animals_generator = animals_generator
        self.human_generator = human_generator



        self.height = 100
        self.width = 100
        self.scale = 100

    def create_world_facade_and_its_adapter(self, width, height, scale) -> tuple[WorldFacade,WorldSnapshotAdapter]:
        world_array = self._generate_map_array(width, height, scale)
        tiles: list[Tile] = TileAdapter.to_tiles(world_array)
        id_registry = IdRegistry()
        world_map = WorldMap(1,"Brave new world", width, height, tiles, id_registry)
        world_state_service = WorldStateService(id_registry, width, height)
        world_interactions_validator_protocol = WorldInteractionsValidator(world_map, world_state_service)
        world_perception_adapter = WorldPerceptionAdapter(world_state_service, world_map,world_interactions_validator_protocol,id_registry)
        vision_port = VisionPort(world_perception_adapter, world_map.width, world_map.height)
        world_facade = WorldFacade(world_map,
                                           world_state_service,
                                           vision_port,
                                           world_perception_adapter,
                                           world_interactions_validator_protocol,
                                           id_registry,
                                           self.event_bus)
        world_facade = self._generate_plants(world_facade)
        world_facade = self._generate_animals(world_facade)
        world_facade = self._generate_humans(world_facade)
        world_snapshot_adapter = WorldSnapshotAdapter(world_state_service, world_map)

        return world_facade, world_snapshot_adapter


    def _generate_map_array(self, width, height, scale):

        self.height = height
        self.width = width
        self.scale = scale

        self.logger.info("Generating world started ...")
        world = np.zeros((height, width), dtype=np.float32)

        for y in tqdm(range(height), desc="Generating world"):
            for x in range(width):
                nx = x / self.scale
                ny = y / self.scale
                world[y][x] = self.elevation_generator.generate_elevation(nx, ny)

        self.logger.info("Finished generating world")

        return world

    def _generate_plants(self, world_facade: WorldFacade) -> WorldFacade:
        self.logger.info("Generating plants started ...")
        world_facade = self.plants_generator.generate_plants(world_facade)
        self.logger.info("Finished generating plants")
        return world_facade

    def _generate_animals(self, world_facade: WorldFacade) -> WorldFacade:
        self.logger.info("Generating animals started ...")
        world_facade = self.animals_generator.generate(world_facade)
        self.logger.info("Finished generating animals")
        return world_facade

    def _generate_humans(self, world_facade: WorldFacade) -> WorldFacade:
        self.logger.info("Generating humans started ...")
        world_facade = self.human_generator.generate(world_facade)
        self.logger.info("Finished generating humans")
        return world_facade

    def __normalize_latitude(self, y: int) -> float:
        center = self.height / 2
        distance_from_equator = abs(y - center)
        return distance_from_equator / center



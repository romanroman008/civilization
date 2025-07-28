import numpy as np
from tqdm import tqdm

from domain.services.generators.human_generator import HumanGenerator
from domain.world_map.tile import Tile
from domain.world_map.world_map import WorldMap
from domain.services.generators.animals_generator import AnimalsGenerator
from domain.services.generators.elevation_generator import ElevationGenerator
from domain.services.generators.plants_generator import PlantsGenerator
from domain.services.tile_adapter import TileAdapter


class WorldGenerator:

    def __init__(self,
                 logger,
                 elevation_generator: ElevationGenerator,
                 plants_generator: PlantsGenerator,
                 animals_generator: AnimalsGenerator,
                 human_generator: HumanGenerator
                 ):

        self.logger = logger

        self.elevation_generator = elevation_generator
        self.plants_generator = plants_generator
        self.animals_generator = animals_generator
        self.human_generator = human_generator

        self.height = 100
        self.width = 100
        self.scale = 100

    def create(self, width, height, scale) -> WorldMap:
        world_array = self._generate_map_array(width, height, scale)
        tiles: list[Tile] = TileAdapter.to_tiles(world_array)
        world = WorldMap(1,"Brave new world", width, height, tiles)
       # world = self._generate_plants(world)
        world = self._generate_animals(world)
        world = self._generate_humans(world)

        return world

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

    def _generate_plants(self, world: WorldMap) -> WorldMap:
        self.logger.info("Generating plants started ...")
        world = self.plants_generator.generate_plants(world)
        self.logger.info("Finished generating plants")
        return world

    def _generate_animals(self, world: WorldMap) -> WorldMap:
        self.logger.info("Generating animals started ...")
        world = self.animals_generator.generate(world)
        self.logger.info("Finished generating animals")
        return world

    def _generate_humans(self, world: WorldMap) -> WorldMap:
        self.logger.info("Generating humans started ...")
        world = self.human_generator.generate(world)
        self.logger.info("Finished generating humans")
        return world

    def __normalize_latitude(self, y: int) -> float:
        center = self.height / 2
        distance_from_equator = abs(y - center)
        return distance_from_equator / center

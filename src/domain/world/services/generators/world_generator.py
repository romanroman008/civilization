import numpy as np
from tqdm import tqdm

from domain.world.entieties.tile import Tile
from domain.world.entieties.world import WorldMap
from domain.world.services.generators.elevation_generator import ElevationGenerator
from domain.world.services.tile_adapter import TileAdapter


class WorldGenerator:

    def __init__(self, logger, elevation_generator: ElevationGenerator):
        self.logger = logger
        self.elevation_generator = elevation_generator

        self.height = 100
        self.width = 100
        self.scale = 100

    def create(self, width, height, scale) -> WorldMap:
        world_array = self._generate_map_array(width, height, scale)
        tiles: list[Tile] = TileAdapter.to_tiles(world_array)
        world = WorldMap("Brave new world", width, height, tiles)

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

    def __normalize_latitude(self, y: int) -> float:
        center = self.height / 2
        distance_from_equator = abs(y - center)
        return distance_from_equator / center

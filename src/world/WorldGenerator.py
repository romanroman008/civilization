
import numpy as np
from tqdm import tqdm

from world.generators.ElevationGenerator import ElevationGenerator



class WorldGenerator:

    def __init__(self, logger, elevation_generator: ElevationGenerator):
        self.logger = logger
        self.elevation_generator = elevation_generator


        self.height = 100
        self.width = 100
        self.scale = 100


    def generate_map(self, width, height, scale):

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












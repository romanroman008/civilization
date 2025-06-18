import math

import numpy as np

from opensimplex import OpenSimplex

from tools.Utils import normalize, normalize_layered_noise
from world.biome.BiomeClassifier import BiomeClassifier


class WorldGenerator:

    def __init__(self, logger, biome_class:BiomeClassifier):
        self.logger = logger

        self.biome_class = biome_class

        self.layers = [
            {"frequency": 1.0, "amplitude": 1.0},
            {"frequency": 2.0, "amplitude": 0.5},
            {"frequency": 4.0, "amplitude": 0.25},
        ]
        self.height = 1
        self.width = 1

        self.elevation_seed = 43
        self.elevation_noise = None

        self.moisture_noise_seed = 29
        self.moisture_noise = None

        self.elevation_power = 1.5
        self.scale = 75





    def generate_map(self, width, height):
        self.elevation_noise = OpenSimplex(self .elevation_seed)
        self.moisture_noise = OpenSimplex(self.moisture_noise_seed)
        self.height = height
        self.width = width

        world = np.zeros((height, width, 3), dtype=np.float32)
        biome_map = np.empty((height, width), dtype = object)
        self.logger.info("Generating world ...")


        for y in range(height):
            for x in range(width):

                nx = x / self.scale
                ny = y / self.scale
                elevation_init = 0
                moisture_init = 0
                amplitudes_sum = 0

                elevation = self._generate_elevation(elevation_init, amplitudes_sum, nx, ny)
                moisture = self._generate_moisture(moisture_init, amplitudes_sum, nx, ny)
                temperature = self._generate_temperature(y)
                biome =  self.biome_class.classify(self.__normalize_latitude(y), temperature, elevation, moisture)

                world[y][x][0] = elevation
                world[y][x][1] = temperature
                world[y][x][2] = moisture

                biome_map[y][x] = biome



        self.logger.info("Finished generating world")
        return world, biome_map



    def _generate_elevation(self, elevation, amplitudes_sum, nx, ny):
        for layer in self.layers:
            elevation += layer["amplitude"] * self.elevation_noise.noise2(layer["frequency"] * nx, layer["frequency"] * ny)
            amplitudes_sum += layer["amplitude"]
        elevation = normalize_layered_noise(elevation, amplitudes_sum)
        return math.pow(elevation, self.elevation_power)


    def _generate_moisture(self, moisture, amplitudes_sum, nx, ny):
        for layer in self.layers:
            moisture += layer["amplitude"] * self.moisture_noise.noise2(layer["frequency"] * nx, layer["frequency"] * ny)
            amplitudes_sum += layer["amplitude"]
        return normalize_layered_noise(moisture, amplitudes_sum)


    def _generate_temperature(self, y):
        temperature = abs(y - self.height / 2)
        temperature = normalize(temperature, 0, self.height / 2)
        return 1.0 - temperature

    def __normalize_latitude(self, y: int) -> float:
        center = self.height / 2
        distance_from_equator = abs(y - center)
        return distance_from_equator / center












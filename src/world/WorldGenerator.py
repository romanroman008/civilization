import math

import noise
import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2
from opensimplex import OpenSimplex


class WorldGenerator:

    def __init__(self, logger):
        self.logger = logger
        self.layers = [
            {"frequency": 1.0, "amplitude": 1.0},
            {"frequency": 2.0, "amplitude": 0.5},
            {"frequency": 4.0, "amplitude": 0.25},
        ]
        self.elevation_seed = 999
        self.moisture_noise_seed = 29
        self.elevation_power = 1.5
        self.scale = 75.0
        self.elevation_noise = None
        self.moisture_noise = None


    def generate_map(self, width, height):
        self.elevation_noise = OpenSimplex(self.elevation_seed)
        self.moisture_noise = OpenSimplex(self.moisture_noise_seed)

        world = np.zeros((height, width, 3), dtype=np.float32)
        self.logger.info("Generating heightmap ...")


        for y in range(height):
            for x in range(width):

                nx = x / self.scale
                ny = y / self.scale
                elevation_init = 0
                moisture_init = 0
                amplitudes_sum = 0

                elevation = self._generate_elevation(elevation_init, amplitudes_sum, nx, ny)
                moisture = self._generate_moisture(moisture_init, amplitudes_sum, nx, ny)
                temperature = 1

                world[y][x][0] = elevation
                world[y][x][1] = temperature
                world[y][x][2] = moisture


        self.logger.info("Finished generating heightmap")
        return world



    def _generate_elevation(self, elevation, amplitudes_sum, nx, ny):
        for layer in self.layers:
            elevation += layer["amplitude"] * self.elevation_noise.noise2(layer["frequency"] * nx, layer["frequency"] * ny)
            amplitudes_sum += layer["amplitude"]
        elevation = self._normalize_elevation(elevation, amplitudes_sum)
        return math.pow(elevation, self.elevation_power)




    def _generate_moisture(self, moisture, amplitudes_sum, nx, ny):
        for layer in self.layers:
            moisture += layer["amplitude"] * self.moisture_noise.noise2(layer["frequency"] * nx, layer["frequency"] * ny)
            amplitudes_sum += layer["amplitude"]
        return self._normalize_elevation(moisture, amplitudes_sum)






    def _normalize_elevation(self, value, amplitudes_sum):
        value = value/amplitudes_sum
        return (value + 1) / 2

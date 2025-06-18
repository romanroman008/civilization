import math

from world.generators.noise import NoiseGenerator


class ElevationGenerator:
    def __init__(self, noise_generator:NoiseGenerator):
        self.noise_generator = noise_generator
        self.elevation_power = 1.5



    def generate_elevation(self, x, y):
        return math.pow(self.noise_generator.noise2(x,y), self.elevation_power)





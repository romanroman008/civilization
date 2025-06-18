import math

from world.generators.noise import NoiseGenerator


class ElevationGenerator:
    def __init__(self, noise_generator:NoiseGenerator):
        self.__noise_generator = noise_generator
        self.__elevation_power = 1.5


    def generate_elevation(self, x, y):
        return math.pow(self.__noise_generator.noise2(x,y), self.__elevation_power)


    def set_elevation_power(self, power):
        self.__elevation_power = power



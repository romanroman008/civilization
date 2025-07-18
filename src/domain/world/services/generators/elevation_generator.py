import math


from domain.world.services.generators.noise.noise_generator import NoiseGenerator


class ElevationGenerator:
    def __init__(self, noise_generator: NoiseGenerator, elevation_power: float = 1.5):
        self._noise_generator = noise_generator
        self._elevation_power = elevation_power


    def generate_elevation(self, x, y):
        return math.pow(self._noise_generator.noise2(x,y), self._elevation_power)


    def set_elevation_power(self, power):
        self._elevation_power = power



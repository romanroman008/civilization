from logging import Logger

from domain.world.services.generators.animals_generator import AnimalsGenerator
from domain.world.services.generators.elevation_generator import ElevationGenerator
from domain.world.services.generators.plants_generator import PlantsGenerator
from domain.world.services.generators.world_generator import WorldGenerator
from domain.world.services.generators.noise.noise_generator import NoiseGenerator
from domain.world.services.generators.noise.open_simplex_noise_generator import OpenSimplexNoiseGenerator


def create_elevation_noise_generator(cfg: dict) -> NoiseGenerator:
    noise_generator = OpenSimplexNoiseGenerator()
    noise_generator.set_seed(cfg["elevation_seed"])
    noise_generator.set_octaves(cfg["elevation_octaves"])
    return noise_generator

def create_world_generator(logger: Logger,
                           elevation_generator:ElevationGenerator,
                           plants_generator: PlantsGenerator,
                           animals_generator: AnimalsGenerator) -> WorldGenerator:
    return WorldGenerator(logger, elevation_generator,plants_generator, animals_generator)



def create_elevation_generator(noise_generator: NoiseGenerator, cfg: dict) -> ElevationGenerator:
    elevation_generator = ElevationGenerator(noise_generator)
    elevation_generator.set_elevation_power(cfg["elevation_power"])
    return elevation_generator
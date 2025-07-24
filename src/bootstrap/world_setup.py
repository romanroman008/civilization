from logging import Logger

from domain.services.generators.human_generator import HumanGenerator
from domain.world_map.world_map import WorldMap
from domain.services.generators.animals_generator import AnimalsGenerator

from domain.services.generators.elevation_generator import ElevationGenerator
from domain.services.generators.noise.noise_generator import NoiseGenerator
from domain.services.generators.noise.octave import Octave
from domain.services.generators.plants_generator import PlantsGenerator
from domain.services.generators.world_generator import WorldGenerator

from domain.services.generators.noise.open_simplex_noise_generator import OpenSimplexNoiseGenerator
from domain.services.movement.movement_system import MovementSystem

from domain.services.world_service import WorldService
from shared.config import CONFIG, PLANTS_DIST, ANIMALS_DIST, HUMAN_DIST


def create_elevation_noise_generator(elevation_seed: int, elevation_octaves: list[Octave]) -> NoiseGenerator:
    noise_generator = OpenSimplexNoiseGenerator()
    noise_generator.set_seed(elevation_seed)
    noise_generator.set_octaves(elevation_octaves)
    return noise_generator

def create_world_generator(logger: Logger) -> WorldGenerator:
    noise_generator = create_elevation_noise_generator(CONFIG["elevation_seed"], CONFIG["elevation_octaves"])
    elevation_generator = create_elevation_generator(noise_generator, CONFIG["elevation_power"])

    plants_generator = create_plant_generator(CONFIG["plants_count"], PLANTS_DIST)
    animals_generator = create_animal_generator(CONFIG["animals_count"], ANIMALS_DIST)
    human_generator = create_human_generator(CONFIG["human_count"], HUMAN_DIST)
    return WorldGenerator(logger, elevation_generator,plants_generator, animals_generator, human_generator)



def create_elevation_generator(noise_generator: NoiseGenerator, elevation_power) -> ElevationGenerator:
    elevation_generator = ElevationGenerator(noise_generator)
    elevation_generator.set_elevation_power(elevation_power)
    return elevation_generator

def create_plant_generator(count, plant_dist) -> PlantsGenerator:
    return PlantsGenerator(count, plant_dist)

def create_animal_generator(count, animal_dist) -> AnimalsGenerator:
    return AnimalsGenerator(count, animal_dist)

def create_human_generator(count, human_dist) -> HumanGenerator:
    return HumanGenerator(count, human_dist)

def create_world_service(world_generator: WorldGenerator):
    return WorldService(world_generator)

def create_movement_system(logger, world_map: WorldMap):
    return MovementSystem(logger, world_map)
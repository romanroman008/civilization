from logging import Logger
from pathlib import Path

import numpy as np
from opensimplex import OpenSimplex

from tools.logger import get_logger
from tools.paths import get_data_path
from world.Visualisation import show_layer, visualize_biome_map

from world.WorldGenerator import  WorldGenerator
from world.biome.Biome import Biome
from world.biome.BiomeClassifier import BiomeClassifier
from world.biome.BiomeRepository import BiomeRepository
from world.climate.ClimateClassifier import ClimateClassifier
from world.climate.ClimateZoneRepository import ClimateZoneRepository
from world.climate.LatitudeBasedClimateClassifier import LatitudeBasedClimateClassifier
from world.generators.ElevationGenerator import ElevationGenerator
from world.generators.noise.NoiseGenerator import NoiseGenerator
from world.generators.noise.Octave import Octave
from world.generators.noise.OpenSimplexNoiseGenerator import OpenSimplexNoiseGenerator
from world.layers.WorldLayer import WorldLayer

config = {
    "height": 200,
    "width": 200,
    "scale": 75,
    "climate_zones": "climate_zones.json",
    "elevation_seed": 12,
    "elevation_power": 1.5,
    "elevation_octaves": [
        Octave(frequency=1.0, amplitude=1.0),
        Octave(frequency=2.0, amplitude=0.5),
        Octave(frequency=4.0, amplitude=0.25),
    ]
}


def main():
    logger = get_logger("civilization")
    climate_repository = create_climate_repository(config)
    climate_classifier = create_climate_classifier(climate_repository)
    elevation_noise_generator = create_elevation_noise_generator(config)
    elevation_generator = create_elevation_generator(elevation_noise_generator,config)
    world_generator = create_world_generator(logger,elevation_generator,climate_classifier)

    world = world_generator.generate_map(config["height"], config["width"], config["scale"])



    show_layer(create_terrain_layer(world))






def create_elevation_noise_generator(cfg: dict) -> NoiseGenerator:
    noise_generator = OpenSimplexNoiseGenerator()
    noise_generator.set_seed(cfg["elevation_seed"])
    noise_generator.set_octaves(cfg["elevation_octaves"])
    return noise_generator

def create_climate_repository(cfg: dict) -> ClimateZoneRepository:
    return ClimateZoneRepository.from_json(get_data_path(cfg["climate_zones"]))

def create_climate_classifier(repository: ClimateZoneRepository) -> ClimateClassifier:
    return  LatitudeBasedClimateClassifier(repository)

def create_world_generator(logger: Logger, elevation_generator:ElevationGenerator, climate_classifier:ClimateClassifier) -> WorldGenerator:
    return WorldGenerator(logger, elevation_generator, climate_classifier)

def create_elevation_generator(noise_generator: NoiseGenerator, cfg: dict) -> ElevationGenerator:
    elevation_generator = ElevationGenerator(noise_generator)
    elevation_generator.set_elevation_power(cfg["elevation_power"])
    return elevation_generator


def create_terrain_layer(values: np.ndarray):
    return WorldLayer.from_type("Height", values)

def create_temperature_layer(values: np.ndarray):
    return WorldLayer.from_type("Temperature", values)

def create_moisture_layer(values: np.ndarray):
    return WorldLayer.from_type("Moisture", values)



if __name__ == "__main__":
    main()

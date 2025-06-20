from logging import Logger

import numpy as np
import pygame

from config.constans import SCREEN_WIDTH, SCREEN_HEIGHT
from infrastructure.MapAdapter import MapAdapter
from tools.logger import get_logger
from tools.paths import get_data_path
from view.Camera import Camera
from view.TilePrezenter import TilePresenter
from view.WorldRenderer import WorldRenderer
from visualization.Preview import show_layer
from visualization.layers.WorldLayer import WorldLayer

from world.WorldGenerator import  WorldGenerator
from world.climate.ClimateClassifier import ClimateClassifier
from world.climate.ClimateZoneRepository import ClimateZoneRepository
from world.climate.LatitudeBasedClimateClassifier import LatitudeBasedClimateClassifier
from world.generators.ElevationGenerator import ElevationGenerator
from world.generators.noise.NoiseGenerator import NoiseGenerator
from world.generators.noise.Octave import Octave
from world.generators.noise.OpenSimplexNoiseGenerator import OpenSimplexNoiseGenerator


config = {
    "height": 200,
    "width": 200,
    "scale": 50,
    "climate_zones": "climate_zones.json",
    "elevation_seed": 1200,
    "elevation_power": 2,
    "elevation_octaves": [
        Octave(frequency=1.0, amplitude=1.0),
        Octave(frequency=2.0, amplitude=0.5),
        Octave(frequency=4.0, amplitude=0.25),
    ]
}

KEY_BINDINGS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
}


def main():
    logger = get_logger("civilization")
    climate_repository = create_climate_repository(config)
    climate_classifier = create_climate_classifier(climate_repository)
    elevation_noise_generator = create_elevation_noise_generator(config)
    elevation_generator = create_elevation_generator(elevation_noise_generator,config)
    world_generator = create_world_generator(logger,elevation_generator,climate_classifier)

    world = world_generator.generate_map(config["height"], config["width"], config["scale"])

    run_game(world)


    show_layer(create_terrain_layer(world))



def run_game(world):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Civilization")

    tile_presenter = TilePresenter()
    map_adapter = MapAdapter(world)
    camera = Camera(0,0,SCREEN_WIDTH,SCREEN_HEIGHT, config["width"], config["width"])
    world_renderer = WorldRenderer(screen,map_adapter,tile_presenter)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        keys = pygame.key.get_pressed()
        for key, (dx,dy) in KEY_BINDINGS.items():
            if keys[key]:
                camera.move(dx,dy)
            # Aktualizacja i render
        screen.fill((0, 0, 0))
        world_renderer.render_map(camera)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


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

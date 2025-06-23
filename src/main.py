from logging import Logger

import numpy as np
import pygame


from infrastructure.MapAdapter import MapAdapter
from tools.logger import get_logger

from view.Camera import Camera
from view.TilePrezenter import TilePresenter
from view.WorldRenderer import WorldRenderer
from visualization.Preview import show_layer
from visualization.layers.WorldLayer import WorldLayer

from world.WorldGenerator import  WorldGenerator
from world.generators.ElevationGenerator import ElevationGenerator
from world.generators.noise.NoiseGenerator import NoiseGenerator
from world.generators.noise.Octave import Octave
from world.generators.noise.OpenSimplexNoiseGenerator import OpenSimplexNoiseGenerator


CONFIG = {
    "screen_width": 2000,
    "screen_height": 1000,
    "tile_size": 16,
    "fps": 60,
    "map_height": 200,
    "map_width": 200,
    "scale": 50,
    "climate_zones": "climate_zones.json",
    "elevation_seed": 1200,
    "elevation_power": 2,
    "elevation_octaves": [
        Octave(1.0, 1.0),
        Octave(2.0, 0.5),
        Octave(4.0, 0.25),
    ],
}

KEY_BINDINGS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
}


def main():
    logger = get_logger("civilization")

    elevation_noise_generator = create_elevation_noise_generator(CONFIG)
    elevation_generator = create_elevation_generator(elevation_noise_generator,CONFIG)
    world_generator = create_world_generator(logger,elevation_generator)

    world = world_generator.generate_map(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])

    show_layer(create_terrain_layer(world))

    run_game(world)





def run_game(world):
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Civilization")

    tile_presenter = TilePresenter()
    map_adapter = MapAdapter(world)
    camera = Camera(0,0,CONFIG["screen_width"],CONFIG["screen_height"], CONFIG["map_height"], CONFIG["map_height"])
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

def create_world_generator(logger: Logger, elevation_generator:ElevationGenerator) -> WorldGenerator:
    return WorldGenerator(logger, elevation_generator)

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

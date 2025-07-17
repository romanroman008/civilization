import pygame

from domain.world.services.generators.noise.octave import Octave

CONFIG = {
    "screen_width": 2000,
    "screen_height": 1000,
    "tile_size": 32,
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


DEFAULT_KEY_BINDINGS = {
    "move_up": "w",
    "move_down": "s",
    "move_left": "a",
    "move_right": "d",
}

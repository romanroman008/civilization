
from domain.components.terrain import Terrain
from domain.organism.prefabs.organism_prefab import OrganismPrefab

from domain.services.generators.noise.octave import Octave

CONFIG = {
    "screen_width": 2000,
    "screen_height": 1000,
    "tile_size": 32,
    "fps": 60,
    "map_height": 100,
    "map_width": 100,
    "scale": 50,
    "climate_zones": "climate_zones.json",
    "elevation_seed": 1200,
    "elevation_power": 2,
    "elevation_octaves": [
        Octave(1.0, 1.0),
        Octave(2.0, 0.5),
        Octave(4.0, 0.25),
    ],
    "animals_count": 3,
    "plants_count": 0,
}


DEFAULT_KEY_BINDINGS = {
    "move_up": "w",
    "move_down": "s",
    "move_left": "a",
    "move_right": "d",
}

PLANTS_DIST = [
    (OrganismPrefab(name="Berries", allowed_terrains={Terrain.GRASS}), 1),
    (OrganismPrefab(name="Tree", allowed_terrains={Terrain.GRASS}, block_radius=1), 1)
]

ANIMALS_DIST = [
    (OrganismPrefab(name="Rabbit", allowed_terrains={Terrain.GRASS}), 1)
]

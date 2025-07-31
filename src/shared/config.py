
from domain.components.terrain import Terrain
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.organism.prefabs.plant_prefab import PlantPrefab

from domain.services.generators.noise.octave import Octave

CONFIG = {
    "screen_width": 800,
    "screen_height": 600,
    "tile_size": 32,
    "fps": 60,
    "map_height":5,
    "map_width": 10,
    "scale": 50,
    "climate_zones": "climate_zones.json",
    "elevation_seed": 1200,
    "elevation_power": 2,
    "elevation_octaves": [
        Octave(1.0, 1.0),
        Octave(2.0, 0.5),
        Octave(4.0, 0.25),
    ],
    "animals_count": 0,
    "plants_count": 1,
    "human_count": 1,
    "human_vision_radius": 5
}


DEFAULT_KEY_BINDINGS = {
    "move_up": "w",
    "move_down": "s",
    "move_left": "a",
    "move_right": "d",
}

PLANTS_DIST = [
    (PlantPrefab(name="Berries", allowed_terrains={Terrain.GRASS}, is_edible = True), 1),
    (PlantPrefab(name="Tree", allowed_terrains={Terrain.GRASS},is_edible = False, block_radius=1), 1)
]

ANIMALS_DIST = [
    (OrganismPrefab(name="Rabbit", allowed_terrains={Terrain.GRASS}), 1)
]

HUMAN_DIST = [
    (OrganismPrefab(name="Human", allowed_terrains={Terrain.GRASS}), 1)
]

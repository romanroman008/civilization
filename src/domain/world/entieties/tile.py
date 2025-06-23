from dataclasses import dataclass

from domain.world.entieties.terrain import Terrain


@dataclass
class Tile:
    tile_id: int
    x: int
    y: int
    terrain: Terrain


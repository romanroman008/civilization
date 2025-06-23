from dataclasses import dataclass, field

from infrastructure.Terrain import Terrain


@dataclass
class Tile:
    tile_id: int
    x: int
    y: int
    terrain: Terrain


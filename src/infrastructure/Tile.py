from dataclasses import dataclass, field

from infrastructure.Biome import Biome


@dataclass
class Tile:
    tile_id: int
    x: int
    y: int
    biome: Biome
    elevation: float



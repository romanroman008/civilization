from dataclasses import dataclass

from domain.world.entieties.terrain import Terrain


@dataclass
class Tile:
    id: int
    x: int
    y: int
    terrain: Terrain


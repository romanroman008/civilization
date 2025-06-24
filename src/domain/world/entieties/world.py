from dataclasses import dataclass, field
from typing import Sequence, Optional

from domain.world.entieties.tile import Tile


@dataclass
class WorldMap:
    name: str
    width: int
    height: int
    tiles: list[Tile]
    id: Optional[int] = None

    _tile_by_coords: dict[tuple[int, int], Tile] = field(init=False, repr=False)
    _tile_by_id: dict[int, Tile] = field(init=False, repr=False)

    def __post_init__(self):
        self._tile_by_coords = {(t.x, t.y): t for t in self.tiles}
        self._tile_by_id = {t.id: t for t in self.tiles}

    def get_tile_by_coords(self, x: int, y: int) -> Tile:
        return self._tile_by_coords[(x, y)]

    def get_tile_by_id(self, tile_id: int) -> Tile:
        return self._tile_by_id[tile_id]

    def get_all_tiles(self) -> Sequence[Tile]:
        return tuple(self.tiles)

    @classmethod
    def create(cls, name: str, width: int, height: int, tiles: list[Tile]) -> "WorldMap":
        return cls(name=name, width=width, height=height, tiles=tiles)

    @classmethod
    def with_id(cls, id: int, name: str, width: int, height: int, tiles: list[Tile]) -> "WorldMap":
        return cls(id=id, name=name, width=width, height=height, tiles=tiles)

from dataclasses import dataclass, field
from typing import Sequence, Optional

from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.world_map.tile import Tile


def _is_terrain_allowed(tile: Tile, allowed_terrains: set[Terrain]):
    if tile.terrain in allowed_terrains:
        return True
    return False

@dataclass
class WorldMap:
    _id:int
    _name: str
    _width: int
    _height: int
    _tiles: list[Tile]

    _tile_by_coords: dict[tuple[int, int], Tile] = field(init=False, repr=False)

    def __post_init__(self):
        self._tile_by_coords = {(t.x, t.y): t for t in self.tiles}

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def tiles(self) -> Sequence[Tile]:
        return tuple(self._tiles)

    def _get_tile_by_coords(self, x: int, y: int) -> Optional[Tile]:
        if self._are_coords_in_bounds(x, y):
            return self._tile_by_coords[(x, y)]
        return None

    def _are_coords_in_bounds(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_terrain_at_position(self, position: Position) -> Optional[Terrain]:
        tile = self._get_tile_by_coords(position.x, position.y)
        if not tile:
            return None
        return tile.terrain

    def is_position_in_bounds(self, position: Position) -> bool:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return True
        return False

    def is_position_allowed(self, position:Position, allowed_terrains: set[Terrain]) -> bool:
        tile = self._get_tile_by_coords(position.x, position.y)
        if tile is None:
            return False
        return _is_terrain_allowed(tile, allowed_terrains)

    def get_all_renderable(self) -> Sequence[Renderable]:
        renderable = []
        renderable.extend(self.tiles)
        return renderable








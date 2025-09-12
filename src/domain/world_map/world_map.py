from dataclasses import dataclass, field
from typing import Sequence, Optional, Tuple, Iterator

from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.world_map.tile import Tile
from shared.id_registry import IdRegistry


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
    _id_registry: IdRegistry

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


    def get_tiles_at_positions(self, positions: list[Position]) -> list[Tile]:
        tiles = self._tile_by_coords
        collected = []
        append = collected.append

        for x,y in positions:
            tile = tiles.get((x, y))
            if tile:
                append(tile)

        return collected


    def is_position_in_bounds(self, position: Position) -> bool:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return True
        return False

    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool:
        tile = self._get_tile_by_coords(position[0], position[1])
        if tile is None:
            return False
        return _is_terrain_allowed(tile, allowed_terrains)

    def get_all_renderable(self) -> Sequence[Renderable]:
        renderable = []
        renderable.extend(self.tiles)
        return renderable


    def get_tiles_in_viewport(self, start_x, end_x, start_y, end_y) -> Iterator[Tile]:
        width, height = self.width, self.height
        if (not self.is_position_in_bounds(Position(start_x, start_y))
            or not self.is_position_in_bounds(Position(end_x, end_y))):

            start_x, start_y = 0, 0
            end_x, end_y = width, height

        end_x = min(end_x + 1, width - 1)
        end_y = min(end_y + 1, height - 1)

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                yield self._get_tile_by_coords(x, y)











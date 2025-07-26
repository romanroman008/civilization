from dataclasses import field

from domain.components.position import Position
from domain.human.perception.percived_object import PerceivedObject

from domain.world_map.tile import Tile


def _tile_to_perceived_object(observer_position: Position, tile: Tile) -> PerceivedObject:
    return PerceivedObject(tile.position - observer_position, tile.terrain, tile.organism)


class WorldPerception:
    def __init__(self, tiles: list[Tile], width: int, height: int):
        self._tiles = tiles
        self._tile_by_coords: dict[tuple[int, int], Tile] = field(init=False, repr=False)
        self._width: int = width
        self._height: int = height

    def __post_init__(self):
        self._tile_by_coords = {(t.x, t.y): t for t in self._tiles}

    def _get_tile(self, position: Position) -> Tile:
        return self._tile_by_coords[position.x, position.y]

    def _get_tiles(self, positions: list[Position]) -> list[Tile]:
        return [
            tile for position in positions
            if (tile := self._get_tile(position)) is not None
        ]

    def get_visible_area(self, observer_position: Position, positions: list[Position]) -> list[PerceivedObject]:
        perceived_objects = []
        for tile in self._get_tiles(positions):
            perceived_objects.append(_tile_to_perceived_object(observer_position, tile))

        return perceived_objects

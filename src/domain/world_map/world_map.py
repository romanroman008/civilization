from dataclasses import dataclass, field
from typing import Sequence, Optional

from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.organism.instances.organism import Organism
from domain.world_map.tile import Tile


def _is_terrain_allowed(tile, allowed_terrains: set[Terrain]):
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
    _organisms:list[Organism] = field(default_factory=list)

    _tile_by_coords: dict[tuple[int, int], Tile] = field(init=False, repr=False)
    _tile_by_id: dict[int, Tile] = field(init=False, repr=False)

    def __post_init__(self):
        self._tile_by_coords = {(t.x, t.y): t for t in self.tiles}
        self._tile_by_id = {t.id: t for t in self.tiles}

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

    @property
    def organisms(self) -> Sequence[Organism]:
        return tuple(self._organisms)

    def _get_tile_by_coords(self, x: int, y: int) -> Optional[Tile]:
        if self.are_coords_in_bounds(x, y):
            return self._tile_by_coords[(x, y)]
        return None

    def get_tile_by_position(self, position: Position) -> Optional[Tile]:
        return self._get_tile_by_coords(position.x, position.y)

    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool:
        if self.are_coords_in_bounds(position.x, position.y):
            tile = self._get_tile_by_coords(position.x, position.y)
            return (_is_terrain_allowed(tile, allowed_terrains)) and not tile.is_occupied
        return False



    def is_tile_occupied(self, x: int, y: int) -> bool:
        return self._tile_by_coords[(x, y)].is_occupied

    def is_position_occupied(self, position: Position) -> bool:
        return self._tile_by_coords[position.x, position.y].is_occupied

    def are_coords_in_bounds(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def is_position_in_bounds(self, position: Position) -> bool:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return True
        return False


    def is_position_available(self, position: Position) -> bool:
        if (
            self.is_position_in_bounds(position)
            and not self.is_position_occupied(position)
        ):
            return True
        return False

    def add_organism(self, organism: Organism):
        tile = self.get_tile_by_position(organism.position)
        tile.add_organism(organism)
        self._organisms.append(organism)

    def set_as_move_target(self, position: Position):
        if self.is_position_in_bounds(position):
            self._get_tile_by_coords(position.x, position.y).set_as_move_target()


    def get_all_renderable(self) -> Sequence[Renderable]:
        renderable = []
        renderable.extend(self.tiles)
        renderable.extend(self.organisms)
        return renderable


    def _get_tiles_by_positions(self, positions:list[Position]) -> list[Tile]:
        tiles = []
        for position in positions:
            if self.is_position_in_bounds(position):
                tiles.append(self._get_tile_by_coords(position.x, position.y))
        return tiles

    def get_organisms_by_positions(self, positions:list[Position]):
        tiles = self._get_tiles_by_positions(positions)
        organisms = []
        for tile in tiles:
            organisms.append(tile.organism)
        return organisms

    def get_terrains_by_positions(self, positions:list[Position]):
        tiles = self._get_tiles_by_positions(positions)
        terrains = []
        for tile in tiles:
            terrains.append()



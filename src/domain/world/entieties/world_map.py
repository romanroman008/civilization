from dataclasses import dataclass, field
from typing import Sequence, Optional

from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.organism.plant import Plant
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain
from domain.world.entieties.tile import Tile


@dataclass
class WorldMap:
    name: str
    width: int
    height: int
    tiles: list[Tile]
    id: Optional[int] = None
    organisms:list[Organism] = field(default_factory=list)

    _tile_by_coords: dict[tuple[int, int], Tile] = field(init=False, repr=False)
    _tile_by_id: dict[int, Tile] = field(init=False, repr=False)

    def __post_init__(self):
        self._tile_by_coords = {(t.x, t.y): t for t in self.tiles}
        self._tile_by_id = {t.id: t for t in self.tiles}

    def get_tile_by_coords(self, x: int, y: int) -> Tile:
        return self._tile_by_coords[(x, y)]

    def get_tile_by_position(self, position: Position) -> Tile:
        return self.get_tile_by_coords(position.x, position.y)


    def get_all_tiles(self) -> Sequence[Tile]:
        return tuple(self.tiles)


    def is_tile_occupied(self, x: int, y: int) -> bool:
        return self._tile_by_coords[(x, y)].isOccupied

    def is_position_occupied(self, position: Position) -> bool:
        return self._tile_by_coords[position.x, position.y].isOccupied


    def is_tile_in_bounds(self, x: int, y: int) -> bool:
        if self.get_tile_by_coords(x,y):
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
        tile.isOccupied = True
        tile.add_organism(organism)
        self.organisms.append(organism)


    def get_organism_by_position(self, position: Position) -> Optional[Organism]:
        return next((o for o in self.organisms if o.position == position), None)


    def get_all_renderable(self):
        renderable = []
        renderable.extend(self.get_all_tiles())
        renderable.extend(self.organisms)
        return renderable


    @classmethod
    def create(cls, name: str, width: int, height: int, tiles: list[Tile]) -> "WorldMap":
        return cls(name=name, width=width, height=height, tiles=tiles)

    @classmethod
    def with_id(cls, id: int, name: str, width: int, height: int, tiles: list[Tile]) -> "WorldMap":
        return cls(id=id, name=name, width=width, height=height, tiles=tiles)

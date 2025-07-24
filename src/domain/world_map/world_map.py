from dataclasses import dataclass, field
from typing import Sequence


from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.organism.instances.organism import Organism
from domain.world_map.tile import Tile


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

    def get_tile_by_coords(self, x: int, y: int) -> Tile:
        return self._tile_by_coords[(x, y)]

    def get_tile_by_position(self, position: Position) -> Tile:
        return self.get_tile_by_coords(position.x, position.y)


    def is_tile_occupied(self, x: int, y: int) -> bool:
        return self._tile_by_coords[(x, y)].is_occupied

    def is_position_occupied(self, position: Position) -> bool:
        return self._tile_by_coords[position.x, position.y].is_occupied


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




    def get_all_renderable(self) -> Sequence[Renderable]:
        renderable = []
        renderable.extend(self.tiles)
        renderable.extend(self.organisms)
        return renderable




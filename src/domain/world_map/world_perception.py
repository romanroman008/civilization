from dataclasses import field
from typing import Sequence, Optional

from domain.components.position import Position
from domain.human.perception.animal_info import AnimalInfo
from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.organism import Organism

from domain.world_map.tile import Tile


def _tile_to_perceived_object(observer_position: Position, tile: Tile) -> PerceivedObject:
    if tile.organism:
        organism_info = _organism_to_organism_info(observer_position, tile.organism)
        return PerceivedObject(tile.position - observer_position, tile.terrain, organism_info)
    return PerceivedObject(tile.position - observer_position, tile.terrain)



def _organism_to_organism_info(observer_position: Position, organism: Organism) -> OrganismInfo:
    if isinstance(organism, Animal):
        return AnimalInfo(organism.id, organism.position - observer_position)
    return OrganismInfo(organism.id, organism.position - observer_position)


class WorldPerception:
    def __init__(self, tiles: Sequence[Tile], width: int, height: int):
        self._tiles = tiles
        self._width: int = width
        self._height: int = height
        self._tile_by_coords: dict[tuple[int, int], Tile] = {
            (tile.position.x, tile.position.y): tile for tile in tiles
        }

    def __post_init__(self):
        self._tile_by_coords = {(t.x, t.y): t for t in self._tiles}

    def _get_tile(self, position: Position) -> Optional[Tile]:
        if self._is_position_in_bounds(position):
            return self._tile_by_coords[position.x, position.y]
        return None

    def _is_position_in_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self._width and 0 <= position.y < self._height

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

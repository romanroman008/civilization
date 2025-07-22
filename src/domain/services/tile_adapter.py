import numpy as np

from domain.components.terrain import Terrain
from domain.entieties.tile import Tile


class TileAdapter:

    @staticmethod
    def to_tiles(world_map_array: np.ndarray[float, float]) -> list[Tile]:
        tiles: list[Tile] = []
        height, width = world_map_array.shape

        for x in range(height):
            for y in range(width):
                value = world_map_array[x, y]
                terrain = TileAdapter.match_biome(value)
                tile_id = x * width + y
                tiles.append(Tile(tile_id, x, y, terrain))

        return tiles

    @staticmethod
    def match_biome(elevation:float) -> Terrain:
        if elevation < 0.20:
            return Terrain.WATER
        return Terrain.GRASS
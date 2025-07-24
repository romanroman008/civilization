import numpy as np

from domain.components.terrain import Terrain
from domain.world_map.tile import Tile


class TileAdapter:

    @staticmethod
    def to_tiles(world_map_array: np.ndarray[float, float]) -> list[Tile]:
        tiles: list[Tile] = []
        height, width = world_map_array.shape

        for y in range(height):
            for x in range(width):
                value = world_map_array[y, x]  # ← NumPy: [row, col]
                terrain = TileAdapter.match_biome(value)
                tile_id = y * width + x
                tiles.append(Tile(tile_id, x, y, terrain))

        return tiles

    @staticmethod
    def match_biome(elevation:float) -> Terrain:
        if elevation < 0.20:
            return Terrain.WATER
        return Terrain.GRASS
import numpy as np

from infrastructure.Terrain import Terrain
from infrastructure.Tile import Tile


class MapAdapter:
    def __init__(self, world_map: np.ndarray[float, float]):
        self._world_map = world_map
        self._tiles_ids = self.generate_ids()

    def get_tile(self, x, y) -> Tile:
        tile_id = self.get_id(x, y)
        biome = self.match_biome(x,y)

        return Tile(tile_id, x, y, biome)

    def match_biome(self, x, y) -> Terrain:
        val = self._world_map[y, x]
        if val < 0.20:
            return Terrain.WATER
        return Terrain.GRASS


    def generate_ids(self) -> np.ndarray:
        h, w = self._world_map.shape
        return np.arange(h * w).reshape((h, w))

    def get_id(self, x, y) -> int:
        return self._tiles_ids[y][x]

    def get_ids_tensor(self):
        readonly = self._tiles_ids.view()
        readonly.setflags(write=False)
        return readonly

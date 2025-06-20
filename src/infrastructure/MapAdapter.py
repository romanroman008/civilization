import numpy as np

from infrastructure.Biome import Biome
from infrastructure.Tile import Tile


class MapAdapter:
    def __init__(self, world_map: np.ndarray[float, float]):
        self._world_map = world_map
        self._tiles_ids = self.generate_ids()

    def get_tile(self, x, y) -> Tile:
        tile_id = self.get_id(x, y)
        elevation = self._world_map[y][x]
        biome = self.match_biome(x,y)

        return Tile(tile_id, x, y, biome, elevation)

    def match_biome(self, x, y) -> Biome:
        val = self._world_map[y, x]
        if val < 0.16:
            return Biome.WATER
        elif val < 0.32:
            return Biome.DARK_GRASS
        elif val < 0.48:
            return Biome.GRASS
        elif val < 0.64:
            return Biome.LIGHT_GRASS
        elif val < 0.80:
            return Biome.SAND
        return Biome.MOUNTAIN

    def generate_ids(self) -> np.ndarray:
        h, w = self._world_map.shape
        return np.arange(h * w).reshape((h, w))

    def get_id(self, x, y) -> int:
        return self._tiles_ids[y][x]

    def get_ids_tensor(self):
        readonly = self._tiles_ids.view()
        readonly.setflags(write=False)
        return readonly

from infrastructure.Tile import Tile
from view.TileView import TileView

TILE_COLORS = {
    1: "#3b83bd",  # WATER – chłodny niebieski
    2: "#355e3b",  # DARK_GRASS – ciemna zieleń
    3: "#4CAF50",  # GRASS – standardowa zieleń
    4: "#8BC34A",  # LIGHT_GRASS – jasna zieleń / oliwkowy
    5: "#f4e19c",  # SAND – piaskowy/beż
    6: "#8B8C7A",  # MOUNTAIN – szarobrązowy (skały)
}

TILE_COLORS_RGB = {

    1: (59, 131, 189),   # WATER
    2: (53, 94, 59),     # DARK_GRASS
    3: (76, 175, 80),    # GRASS
    4: (139, 195, 74),   # LIGHT_GRASS
    5: (244, 225, 156),  # SAND
    6: (139, 140, 122),  # MOUNTAIN
}

class TilePresenter:
    def __init__(self, biome_colors=None):
        if biome_colors is None:
            biome_colors = TILE_COLORS_RGB
        self._biome_colors = biome_colors



    def present(self, tile: Tile) -> TileView:
        color = self._biome_colors[tile.biome.value]
        return TileView(tile.tile_id, color)


from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position
from domain.world.entieties.renderable import Renderable
from domain.world.entieties.terrain import Terrain
from domain.world.entieties.tile import Tile
from domain.world.entieties.world_map import WorldMap
from infrastructure.rendering.sprite import Sprite
from infrastructure.rendering.sprite_asset import SpriteAsset
from infrastructure.rendering.tile_view import TileView

TILE_COLORS = {
    1: "#3b83bd",  # WATER – chłodny niebieski
    2: "#355e3b",  # DARK_GRASS – ciemna zieleń
    3: "#4CAF50",  # GRASS – standardowa zieleń
    4: "#8BC34A",  # LIGHT_GRASS – jasna zieleń / oliwkowy
    5: "#f4e19c",  # SAND – piaskowy/beż
    6: "#8B8C7A",  # MOUNTAIN – szarobrązowy (skały)
}

TILE_COLORS_RGB = {

    Terrain.WATER: (59, 131, 189),   # WATER
    Terrain.GRASS: (76, 175, 80)  # GRASS

}

sprite_assets = {
    "GRASS": SpriteAsset("GRASS", "assets/terrain/grass.png", (1,1), (0,0), 0),
    "WATER": SpriteAsset("WATER", "assets/terrain/water.png", (1,1), (0,0), 0),
    "Tree": SpriteAsset("TREE", "assets/plants/tree.png", (3, 3), (1, 1), 2),
    "Berries":SpriteAsset("BERRY", "assets/plants/berry.png", (1, 1), (0, 0), 1),
    "Rabbit":SpriteAsset("RABBIT", "assets/animals/rabbit.png", (1, 1), (0, 0), 1),

}


class WorldPresenter:
    def __init__(self, world_map: WorldMap):
        self.world_map = world_map
        self.sprite_assets = sprite_assets




    def present(self, entity: Renderable):
        sprite_key = entity.sprite_key
        position = entity.position

        if sprite_key not in self.sprite_assets:
            raise ValueError(f"Unknown sprite key: '{sprite_key}'")

        return Sprite(self.sprite_assets[sprite_key], position)




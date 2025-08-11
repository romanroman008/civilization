
from domain.components.renderable import Renderable

from domain.components.terrain import Terrain
from domain.organism.instances.animal import Animal
from domain.organism.instances.organism import Organism
from infrastructure.rendering.sprite.sprite import Sprite
from infrastructure.rendering.sprite.sprite_asset import SpriteAsset


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
    "GRASS": SpriteAsset("Grass", "assets/terrain/grass.png", (1,1), (0,0), 0),
    "WATER": SpriteAsset("Water", "assets/terrain/water.png", (1,1), (0,0), 0),
    "Tree": SpriteAsset("Tree", "assets/plants/tree.png", (3, 3), (1, 1), 2),
    "BERRIES":SpriteAsset("Berry", "assets/plants/berry.png", (1, 1), (0, 0), 1),
    "RABBIT":SpriteAsset("Rabbit", "assets/animals/rabbit.png", (1, 1), (0, 0), 2),
    "RABBIT_DEAD": SpriteAsset("Dead rabbit", "assets/animals/rabbit_dead.png", (1, 1), (0, 0), 2),
    "HUMAN":SpriteAsset("Human", "assets/human/human.png", (1, 1), (0, 0), 2),
    "RESERVED": SpriteAsset("reserved", "assets/terrain/reserved.png", (1, 1), (0, 0), 0),
    "OCCUPIED": SpriteAsset("occupied", "assets/terrain/occupied.png", (1, 1), (0, 0), 0),

}




class WorldPresenter:
    def __init__(self):
        self.sprite_assets = sprite_assets

    def present(self, entity: Renderable):
        sprite_key = entity.sprite_key
        position = entity.position
        rotation = getattr(entity, "rotation", 0.0)
        offset = getattr(entity, "offset", (0.0,0.0))


        if isinstance(entity, Animal):
            if not entity.is_alive:
                sprite_key += "_DEAD"



        if sprite_key not in self.sprite_assets:
            raise ValueError(f"Unknown sprite key: '{sprite_key}'")

        return Sprite(self.sprite_assets[sprite_key], position, rotation, offset)

    def present_occ(self, entity: Renderable):
        terrain = "OCCUPIED"
        position = entity.position
        rotation = getattr(entity, "rotation", 0.0)
        offset = getattr(entity, "offset", (0.0, 0.0))

        if terrain not in self.sprite_assets:
            raise ValueError(f"Unknown sprite key: '{terrain}'")

        return Sprite(self.sprite_assets[terrain], position, rotation, offset)

    def present_res(self, entity: Renderable):
        terrain = "RESERVED"
        position = entity.position
        rotation = getattr(entity, "rotation", 0.0)
        offset = getattr(entity, "offset", (0.0, 0.0))

        if terrain not in self.sprite_assets:
            raise ValueError(f"Unknown sprite key: '{terrain}'")

        return Sprite(self.sprite_assets[terrain], position, rotation, offset)




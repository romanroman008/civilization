from array import array

import pygame

from domain.components.renderable import Renderable

from domain.components.terrain import Terrain
from domain.organism.instances.animal import Animal
from infrastructure.rendering.camera import Camera

from infrastructure.rendering.soa.organism_soa import OrganismSoA
from infrastructure.rendering.soa.tile_soa import TileSoA
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
    1: SpriteAsset("Grass", "assets/terrain/grass.png", (1,1), (0,0), 0),
    2: SpriteAsset("Water", "assets/terrain/water.png", (1,1), (0,0), 0),
    3: SpriteAsset("Tree", "assets/plants/tree.png", (3, 3), (1, 1), 2),
    4:SpriteAsset("Berry", "assets/plants/berry.png", (1, 1), (0, 0), 1),
    5:SpriteAsset("Rabbit", "assets/animals/rabbit.png", (1, 1), (0, 0), 2),
    "RABBIT_DEAD": SpriteAsset("Dead rabbit", "assets/animals/rabbit_dead.png", (1, 1), (0, 0), 2),
    6:SpriteAsset("Human", "assets/human/human.png", (1, 1), (0, 0), 2),
    "RESERVED": SpriteAsset("reserved", "assets/terrain/reserved.png", (1, 1), (0, 0), 0),
    "OCCUPIED": SpriteAsset("occupied", "assets/terrain/occupied.png", (1, 1), (0, 0), 0),

}





class WorldPresenter:
    def __init__(self, screen_surface: pygame.Surface, tile_size: int, camera: Camera):
        self.sprite_assets = sprite_assets
        self.surface = screen_surface
        self.tile_size = tile_size
        self.camera = camera



    def present_tiles(self, tile_soa: TileSoA, visible_indexes: array):
        xs, ys, sprites = tile_soa.xs, tile_soa.ys, tile_soa.sprites
        tile_size = self.tile_size
        blit = self.surface.blit
        camera_offset_x, camera_offset_y = self.camera.offset_x, self.camera.offset_y

        for i in visible_indexes:
            source = sprite_assets[sprites[i]].image
            dest_rect = pygame.Rect(xs[i] * tile_size - camera_offset_x, ys[i] * tile_size - camera_offset_y, tile_size, tile_size)
            blit(source, dest_rect)


    def preset_organisms(self, organism_soa: OrganismSoA, visible_indexes: array):
        xs, ys = organism_soa.xs, organism_soa.ys
        rots = organism_soa.rots
        sprites, alives = organism_soa.sprites, organism_soa.alives
        blit = self.surface.blit
        tile_size = self.tile_size
        camera_offset_x, camera_offset_y = self.camera.offset_x, self.camera.offset_y




        for i in visible_indexes:
            source = sprite_assets[sprites[i]].image
            px = xs[i] * tile_size - camera_offset_x
            py = ys[i] * tile_size - camera_offset_y


            dest_rect = pygame.Rect(px, py, tile_size, tile_size)
            rotated_source = pygame.transform.rotate(source, -rots[i])
            blit(rotated_source, dest_rect)





    def present_depr(self, entity: Renderable):
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






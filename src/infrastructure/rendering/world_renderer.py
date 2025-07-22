from collections import defaultdict


import pygame

from domain.components.position import Position
from domain.world_map.world_map import WorldMap
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.sprite import Sprite

from infrastructure.rendering.world_presenter import WorldPresenter


class WorldRenderer:
    def __init__(self,
                 surface: pygame.Surface,
                 world_map: WorldMap,
                 world_presenter: WorldPresenter,
                 camera: Camera,
                 chunk_size: int = 16,
                 tile_size: int = 32):
        self.surface = surface
        self.world_map = world_map
        self.world_presenter = world_presenter
        self.camera = camera
        self.chunk_size = chunk_size
        self.tile_size = tile_size

    def render_map(self, camera):

        sprites = self.get_sprites_in_viewport()
        sprites_by_layer = self.get_sprites_by_layer(sprites)

        for layer in sorted(sprites_by_layer.keys()):
            for sprite in sprites_by_layer[layer]:
                anchor_px = self._world_to_screen(sprite.position, camera)
                surface, rect = sprite.get_render(anchor_px, self.tile_size)
                self.surface.blit(surface, rect)

    def _world_to_screen(self, pos: Position, camera: Camera) -> tuple[int, int]:
        return (
            pos.x * self.tile_size - camera.offset_x,
            pos.y * self.tile_size - camera.offset_y
        )

    def get_sprites_in_viewport(self):
        renderables = self.world_map.get_all_renderable()
        start_x, end_x, start_y, end_y = self.camera.get_viewport()
        return [
            self.world_presenter.present(r) for r in renderables
            if start_x <= r.position.x <= end_x and start_y <= r.position.y <= end_y
        ]


    def get_sprites_by_layer(self, sprites: list[Sprite]) -> dict[int, list[Sprite]]:
        grouped = defaultdict(list)
        for sprite in sprites:
            grouped[sprite.asset.layer].append(sprite)
        return grouped

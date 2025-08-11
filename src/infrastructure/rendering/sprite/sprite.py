import pygame

from domain.components.position import Position

from infrastructure.rendering.sprite.sprite_asset import SpriteAsset


class Sprite:
    def __init__(self, asset: SpriteAsset, position: Position, rotation: float, offset: tuple[float, float]):
        self.asset = asset
        self.position = position
        self.rotation = rotation
        self.offset = offset

    def get_render(self, pos: tuple[int, int], tile_size: int) -> tuple[pygame.Surface, pygame.Rect]:
        anchor_px_x = pos[0]
        anchor_px_y = pos[1]

        # Rozmiar sprite’a w pikselach
        sprite_width = self.asset.tile_size[0] * tile_size
        sprite_height = self.asset.tile_size[1] * tile_size

        # Anchor (w tile’ach) × tile_size → offset w pikselach od anchor do lewego górnego rogu
        offset_x = self.asset.anchor[0] * tile_size - self.offset[0] / 100 * tile_size
        offset_y = self.asset.anchor[1] * tile_size - self.offset[1] / 100 * tile_size

        # Lewy górny róg = anchor point - offset
        px = int(anchor_px_x - offset_x)
        py = int(anchor_px_y - offset_y)

        scaled_surface = pygame.transform.scale(self.asset.image, (sprite_width, sprite_height))
        rotated = pygame.transform.rotate(scaled_surface, -self.rotation)

        target_rect = pygame.Rect(px, py, sprite_width, sprite_height)

        return rotated, target_rect
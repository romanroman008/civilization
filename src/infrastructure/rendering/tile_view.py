from dataclasses import dataclass
import pygame
from pygame.examples.grid import TILE_SIZE


@dataclass
class TileView:
    id: int
    layer: int
    color: tuple[int, int, int]
    sprite: pygame.Surface | None = None


    def render(self, surface: pygame.Surface, pos: tuple):
        if self.sprite:
            scaled_sprite = pygame.transform.scale(self.sprite, (TILE_SIZE, TILE_SIZE))
            surface.blit(scaled_sprite, pos)
        else:
            pygame.draw.rect(surface, self.color, (*pos, TILE_SIZE, TILE_SIZE))
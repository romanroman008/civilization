from dataclasses import dataclass
import pygame
from pygame.examples.grid import TILE_SIZE

from domain.world.entieties.tile import Tile


@dataclass
class TileView:
    id: int
    layer: int
    color: tuple[int, int, int]



    def render(self, surface: pygame.Surface, pos: tuple):
        pygame.draw.rect(surface, self.color, (*pos, TILE_SIZE, TILE_SIZE))
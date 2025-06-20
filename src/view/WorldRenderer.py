from typing import List

import pygame

from config.constans import TILE_SIZE
from infrastructure.MapAdapter import MapAdapter

from view.TilePrezenter import TilePresenter




class WorldRenderer:
    def __init__(self, surface: pygame.Surface, map_adapter: MapAdapter, tile_presenter: TilePresenter):
        self.surface = surface
        self.map_adapter = map_adapter
        self.tile_presenter = tile_presenter

    def render_map(self, camera):
        start_x, start_y, width, height = camera.get_viewport()

        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                tile = self.map_adapter.get_tile(x, y)
                tile_view = self.tile_presenter.present(tile)

                world_pos = (x * TILE_SIZE, y * TILE_SIZE)
                screen_pos = (
                    world_pos[0] - camera.offset_x,
                    world_pos[1] - camera.offset_y
                )

                tile_view.render(self.surface, screen_pos)


from array import array
from collections import defaultdict


import pygame


from domain.components.position import Position

from infrastructure.rendering.camera import Camera
from infrastructure.rendering.soa.organism_soa import OrganismSoA
from infrastructure.rendering.soa.tile_soa import TileSoA
from infrastructure.rendering.soa.world_frame_snapshot import WorldFrameSnapshot

from infrastructure.rendering.sprite.sprite import Sprite

from infrastructure.rendering.world_presenter import WorldPresenter
from infrastructure.rendering.world_snapshot_adapter import WorldSnapshotAdapter


def get_sprites_by_layer(sprites: list[Sprite]) -> dict[int, list[Sprite]]:
    grouped = defaultdict(list)
    for sprite in sprites:
        grouped[sprite.asset.layer].append(sprite)
    return grouped




class WorldRenderer:
    def __init__(self,
                 surface: pygame.Surface,
                 camera: Camera,
                 tile_size: int = 32):
        self.surface = surface
        self.world_presenter:WorldPresenter = WorldPresenter(surface, tile_size, camera)
        self.camera = camera
        self.tile_size = tile_size

        self._visible_indexes = array("I")
        self._visible_organisms_indexes = array("I")


    def render_map(self, world_frame_snapshot: WorldFrameSnapshot):
        if not self.world_presenter._map_built:
            self.world_presenter.build_full_map_surface(world_frame_snapshot.tiles)

        self.world_presenter.blit_map_surface_camera_view()
        self.world_presenter.present_organisms_effectively(world_frame_snapshot.organisms)



    def _get_indexes_in_viewport(self, tile_soa: TileSoA) -> array:
        start_x, end_x, start_y, end_y = self.camera.get_viewport()
        xs, ys, sprites = tile_soa.xs, tile_soa.ys, tile_soa.sprites

        n = len(xs)

        idxs = self._visible_indexes
        del idxs[:]

        append = idxs.append

        for i in range(n):
            x = xs[i]
            y = ys[i]
            if start_x <= x <= end_x and start_y <= y <= end_y:
                append(i)

        return idxs

    def _get_organisms_indexes_in_viewport(self, organism_soa: OrganismSoA) -> array:
        start_x, end_x, start_y, end_y = self.camera.get_viewport()
        xs, ys = organism_soa.xs, organism_soa.ys
        n = len(xs)

        idxs = self._visible_organisms_indexes
        del idxs[:]

        append = idxs.append

        for i in range(n):
            x = xs[i]
            y = ys[i]
            if start_x <= x <= end_x and start_y <= y <= end_y:
                append(i)

        return idxs










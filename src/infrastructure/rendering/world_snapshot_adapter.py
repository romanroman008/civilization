from domain.world_map.world_map import WorldMap

from domain.world_map.world_state_service import WorldStateService

from array import array

from infrastructure.rendering.camera import Camera
from infrastructure.rendering.render_utils import render_uid, get_kind_id, get_sprite_id, get_alive_val
from infrastructure.rendering.soa.organism_soa import OrganismSoA
from infrastructure.rendering.soa.tile_soa import TileSoA
from infrastructure.rendering.soa.world_frame_snapshot import WorldFrameSnapshot


#
# | Kod   | Typ w C        | Bajty | Zakres/liczby                   |
# | ----- | -------------- | ----- | ------------------------------- |
# | `'b'` | signed char    | 1     | -128 .. 127                     |
# | `'B'` | unsigned char  | 1     | 0 .. 255                        |
# | `'h'` | signed short   | 2     | -32768 .. 32767                 |
# | `'H'` | unsigned short | 2     | 0 .. 65535                      |
# | `'i'` | signed int     | 4     | -2,147,483,648 .. 2,147,483,647 |
# | `'I'` | unsigned int   | 4     | 0 .. 4,294,967,295              |
# | `'f'` | float          | 4     | zmiennoprzecinkowe 32-bit       |
# | `'d'` | double         | 8     | zmiennoprzecinkowe 64-bit       |




class _OrganismBuffer:
    __slots__ = ("_ids", "_xs", "_ys", "_offset_xs", "_offset_ys",
                 "_rots", "_sprites", "_alives",
                 "append_id", "append_x", "append_y",
                 "append_rot", "append_offset_x", "append_offset_y", "append_spirte", "append_alive")

    def __init__(self):
        self._ids = array("I")
        self._xs = array("f")
        self._ys = array("f")
        self._offset_xs = array("b")
        self._offset_ys = array("b")
        self._rots = array("f")
        self._sprites = array("B")
        self._alives = array("B")
        self._bind_appends()

    def _bind_appends(self):
        self.append_id = self._ids.append
        self.append_x = self._xs.append
        self.append_y = self._ys.append
        self.append_offset_x = self._offset_xs.append
        self.append_offset_y = self._offset_ys.append
        self.append_rot = self._rots.append
        self.append_spirte = self._sprites.append
        self.append_alive = self._alives.append

    def clear(self):
        del self._ids[:]; del self._xs[:]; del self._ys[:]
        del self._rots[:]; del self._offset_xs[:]; del self._offset_ys[:]
        del self._sprites[:]; del self._alives[:]

    def soa(self):
        return OrganismSoA(ids=self._ids, sprites=self._sprites,
                           xs=self._xs, ys=self._ys,
                           offset_xs=self._offset_xs, offset_ys=self._offset_ys, rots=self._rots,
                           alives=self._alives)


class _TileBuffer:
    __slots__ = ("xs", "ys", "sprites",
                 "_ax", "_ay", "_aspr")

    def __init__(self):
        self.xs = array("H")
        self.ys = array("H")
        self.sprites = array("B")
        self._bind_appends()

    def _bind_appends(self):
        self._ax = self.xs.append
        self._ay = self.ys.append
        self._aspr = self.sprites.append

    def clear(self):
        del self.xs[:]; del self.ys[:]; del self.sprites[:]
        #del self._ax[:]; del self._ay[:]; del self._aspr[:]

    def soa(self):
        return TileSoA(xs=self.xs, ys=self.ys, sprites=self.sprites)


class WorldSnapshotAdapter:
    def __init__(self, world_state_service: WorldStateService, world_map: WorldMap):
        self._world_state_service = world_state_service
        self._world_map = world_map
        self._tick_id = 0
        self._time = 0.0

        self._tiles_buf = _TileBuffer()
        self._tiles_buf_alt = _TileBuffer()
        self._organism_buf = _OrganismBuffer()
        self._organism_buf_alt = _OrganismBuffer()
        self._use_alt = False

        self._camera = Camera()

    def set_camera(self, camera: Camera):
        self._camera = camera

    def advance_time(self, tick_id: int, sim_time: float):
        self._tick_id = tick_id
        self._time = sim_time

    def _current_tiles(self) -> _TileBuffer:
        return self._tiles_buf_alt if self._use_alt else self._tiles_buf

    def _current_organisms(self) -> _OrganismBuffer:
        return self._organism_buf_alt if self._use_alt else self._organism_buf

    def _toggle(self):
        self._use_alt = not self._use_alt

    def _adapt_tiles(self, tb: _TileBuffer):
        tb.clear()
        ax, ay, aspr = tb._ax, tb._ay, tb._aspr

        for tile in self._world_map.get_all_renderable():
            ax(tile.position.x)
            ay(tile.position.y)
            aspr(get_sprite_id(tile.sprite_key))

    def _adapt_tiles_viewport(self, tb: _TileBuffer):
        tb.clear()
        ax, ay, aspr = tb._ax, tb._ay, tb._aspr

        start_x, end_x, start_y, end_y = self._camera.get_viewport()

        for tile in self._world_map.get_tiles_in_viewport(start_x, end_x, start_y, end_y):
            ax(tile.position.x)
            ay(tile.position.y)
            aspr(get_sprite_id(tile.sprite_key))



    def _adapt_organisms(self, tb: _OrganismBuffer):
        tb.clear()
        aid, asprite,  = tb.append_id, tb.append_spirte,
        ax, ay, arot = tb.append_x, tb.append_y, tb.append_rot
        aoffx, aoffy = tb.append_offset_x, tb.append_offset_y
        aalive = tb.append_alive

        for organism in self._world_state_service.get_all_organisms():
            aid(render_uid(kind_id=get_kind_id(organism.id.kind), organism_id=organism.id.id))
            ax(organism.x); ay(organism.y)
            aoffx(organism.offset_x); aoffy(organism.offset_y)
            arot(organism.rotation)
            asprite(get_sprite_id(organism.sprite_key))
            aalive(get_alive_val(organism.is_alive))


    def _adapt_organisms_viewport(self, tb: _OrganismBuffer):
        tb.clear()
        aid, asprite, = tb.append_id, tb.append_spirte,
        ax, ay, arot = tb.append_x, tb.append_y, tb.append_rot
        aoffx, aoffy = tb.append_offset_x, tb.append_offset_y
        aalive = tb.append_alive

        start_x, end_x, start_y, end_y = self._camera.get_viewport()

        for organism in self._world_state_service.get_organisms_in_viewport(start_x, end_x, start_y, end_y):
            aid(render_uid(kind_id=get_kind_id(organism.id.kind), organism_id=organism.id.id))
            ax(organism.x)
            ay(organism.y)
            aoffx(organism.offset_x)
            aoffy(organism.offset_y)
            arot(organism.rotation)
            asprite(get_sprite_id(organism.sprite_key))
            aalive(get_alive_val(organism.is_alive))


    def make_snapshot(self, first_load:bool) -> WorldFrameSnapshot:
        tile_buffor = self._current_tiles()
        organism_buffor = self._current_organisms()

        # if camera_moved:
        #     self._adapt_tiles_viewport(tile_buffor)
        #     self._adapt_organisms_viewport(organism_buffor)
        # else:

        if first_load:
            self._adapt_tiles(tile_buffor)

        self._adapt_organisms(organism_buffor)



        snap = WorldFrameSnapshot(
            tick_id=self._tick_id,
            time=self._time,
            tiles= tile_buffor.soa(),
            organisms = organism_buffor.soa()
        )

        self._toggle()

        return snap








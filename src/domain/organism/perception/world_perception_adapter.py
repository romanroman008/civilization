from array import array

from domain.components.position import Position
from domain.organism.perception.perception import Perception
from domain.organism.perception.world_perception_adapter_protocol import WorldPerceptionAdapterProtocol
from domain.world_map.world_interactions_validator_protocol import WorldInteractionsValidatorProtocol
from domain.world_map.world_map import WorldMap
from domain.world_map.world_state_service import WorldStateService
from shared.id_registry import IdRegistry


class _PerceptionBuffer:

    __slots__ = ("_xs", "_ys", "_terrains","_allowed",
                 "_organisms", "_organism_ids", "_organisms_alive",
                 "_offsets_x", "_offsets_y",
                 "append_xs", "append_ys", "append_terrains", "append_allowed",
                 "append_organisms", "append_organism_ids", "append_organisms_alive",
                 "append_offsets_x", "append_offsets_y",)

    def __init__(self):
        self._xs = array("I")
        self._ys = array("I")
        self._terrains = array("H")
        self._allowed = array("B")
        self._organisms = array("H")
        self._organism_ids = array("I")
        self._organisms_alive = array("B")
        self._offsets_x = array("b")
        self._offsets_y = array("b")
        self._bind_appends()


    def _bind_appends(self):
        self.append_xs = self._xs.append
        self.append_ys = self._ys.append
        self.append_terrains = self._terrains.append
        self.append_allowed = self._allowed.append
        self.append_organisms = self._organisms.append
        self.append_organism_ids = self._organism_ids.append
        self.append_organisms_alive = self._organisms_alive.append
        self.append_offsets_x = self._offsets_x.append
        self.append_offsets_y = self._offsets_y.append


    def clear(self):
        del self._xs[:]; del self._ys[:]; del self._terrains[:]; del self._allowed[:]
        del self._organisms[:]; del self._organism_ids[:]; del self._organisms_alive[:]
        del self._offsets_x[:]; del self._offsets_y[:]

    def soa(self):
        return Perception(xs = self._xs, ys = self._ys, terrains = self._terrains, allowed = self._allowed,
                          organisms=self._organisms, organisms_id=self._organism_ids, organisms_alive=self._organisms_alive,
                          offsets_x = self._offsets_x, offsets_y = self._offsets_y)




class WorldPerceptionAdapter(WorldPerceptionAdapterProtocol):
    def __init__(self,
                 world_state_service: WorldStateService,
                 world_map: WorldMap,
                 world_interactions_validator_protocol: WorldInteractionsValidatorProtocol,
                 id_registry: IdRegistry):
        self._world_state_service = world_state_service
        self._world_map = world_map
        self._world_interactions_validator_protocol = world_interactions_validator_protocol
        self._id_registry = id_registry

        self._perception_buffer = _PerceptionBuffer()
        self._perception_buffer_alt = _PerceptionBuffer()

        self._use_alt = False


    def _current_perception(self):
        return self._perception_buffer_alt if self._use_alt else self._perception_buffer

    def _toggle(self):
        self._use_alt = not self._use_alt


    def _adapt_perception(self, positions: list[Position]):
        pb = self._current_perception()
        pb.clear()

        append_xs, append_ys, append_terrains, append_allowed = pb.append_xs, pb.append_ys, pb.append_terrains, pb.append_allowed
        append_organisms, append_organism_ids = pb.append_organisms, pb.append_organism_ids
        append_organism_alive = pb.append_organisms_alive
        append_offsets_x, append_offsets_y = pb.append_offsets_x, pb.append_offsets_y

        get_terrain = self._world_map.get_terrain_at_position
        get_organism = self._world_state_service.get_organism_at_position

        code = self._id_registry.code_object
        is_allowed = self._world_interactions_validator_protocol.is_position_allowed

        for position in positions:
            x, y = position[0], position[1]
            append_xs(x)
            append_ys(y)
            append_terrains(code(get_terrain(Position(x,y))))
            organism = get_organism(Position(x,y))
            if not organism:
                append_organisms(0)
                append_organism_ids(0)
                append_organism_alive(0)
                append_offsets_x(0)
                append_offsets_y(0)

            else:
                organism_id = organism.id
                append_organisms(code(organism.sprite_key))
                append_organism_ids(organism_id.id)
                append_organism_alive(int(organism.is_alive))
                append_offsets_x(int(organism.offset_x))
                append_offsets_y(int(organism.offset_y))

            append_allowed(is_allowed((x,y)))





    def perception_snapshot(self, positions: list[Position]):
        self._adapt_perception(positions)

        perception = self._current_perception().soa()

        self._toggle()

        return perception




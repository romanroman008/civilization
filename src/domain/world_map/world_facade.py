from itertools import chain
from typing import Sequence, Iterable, Optional

from domain.components import position
from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.human.perception.percived_object import PerceivedObject
from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult

from domain.world_map.world_map import WorldMap
from domain.world_map.world_perception import WorldPerception
from domain.world_map.world_state_service import WorldStateService


class WorldFacade:
    def __init__(self, world_map: WorldMap,
                 world_state_service: WorldStateService,
                 world_perception: WorldPerception,
                 event_bus: EventBus):
        self._map = world_map
        self._state_service = world_state_service
        self._world_perception = world_perception
        self._event_bus = event_bus
        self._register_handlers()

    @property
    def height(self) -> int:
        return self._map.height

    @property
    def width(self) -> int:
        return self._map.width

    @property
    def event_bus(self):
        return self._event_bus

    @property
    def world_perception(self):
        return self._world_perception

    def add_organism(self, organism: Organism):
        self._state_service.register_organism(organism)

    def update_position(self, organism: Organism, new_position: Position):
        self._state_service.update_position(organism, new_position)

    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool:
        return (
            self._map.is_position_allowed(position, allowed_terrains)
            and not self._state_service.is_occupied(position)
            and not self._state_service.is_reserved(position)
        )

    def reserve_position(self, position: Position):
        self._state_service.reserve_position(position)

    def get_all_renderable(self) -> Iterable[Renderable]:
        tiles = self._map.get_all_renderable()
        organisms = self._state_service.get_all_renderable()
        return chain(tiles,organisms)


    def _register_handlers(self):
        self._event_bus.on_command("change_state_requested", self._handle_state_change)

    async def _handle_state_change(self, payload, future):
        organism = payload["organism"]
        target_position = payload["target_position"]
        new_state = payload["new_state"]

        result = self._validate_position(target_position, organism.allowed_terrains)
        if result != MoveResult.SUCCESS:
            future.set_result(result)
            return

        self.update_position(organism, target_position)

        await self._event_bus.emit("organism_moved", {
            "organism" : organism,
            "position" : target_position,
        })

        future.set_result(MoveResult.SUCCESS)


    def _validate_position(self, position: Position, terrains: set[Terrain]) -> MoveResult:
        if not self._map.is_position_allowed(position, terrains):
            return MoveResult.OUT_OF_BOUNDS
        if self._state_service.is_occupied(position):
            return MoveResult.OCCUPIED
        if self._state_service.is_reserved(position):
            return MoveResult.RESERVED
        else:
            return MoveResult.SUCCESS


    def get_example_agent(self) -> Optional[Human]:
        return self._state_service.get_example_agent()



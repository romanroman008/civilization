from itertools import chain
from typing import Sequence, Iterable, Optional

from domain.components import position
from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.components.terrain import Terrain
from domain.human.perception.animal_info import AnimalInfo
from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism
from domain.organism.organism_id import OrganismID
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult

from domain.world_map.world_map import WorldMap

from domain.world_map.world_state_service import WorldStateService

def _tile_to_perceived_object(relative_positon: Position, terrain: Terrain, organism:Optional[Organism]) -> PerceivedObject:
    if organism:
        organism_info = _organism_to_organism_info(relative_positon, organism)
        return PerceivedObject(relative_positon, terrain, organism_info)
    return PerceivedObject(relative_positon, terrain, None)

def _organism_to_organism_info(relative_position: Position, organism: Organism) -> OrganismInfo:
    if isinstance(organism, Animal):
        return AnimalInfo(organism.id, relative_position)
    return OrganismInfo(organism.id, relative_position)


class WorldFacade:
    def __init__(self, world_map: WorldMap,
                 world_state_service: WorldStateService,
                 event_bus: EventBus):
        self._map = world_map
        self._state_service = world_state_service
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

    def add_organism(self, organism: Organism):
        self._state_service.register_organism(organism)

    def update_position(self, organism_id: OrganismID, new_position: Position):
        self._state_service.update_position(organism_id, new_position)

    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool:
        return (
            self._map.is_position_allowed(position, allowed_terrains)
            and not self._state_service.is_occupied(position)
            and not self._state_service.is_reserved(position)
        )

    def reserve_position(self, position: Position):
        self._state_service.reserve_position(position)

    def get_visible_area(self, observer_position, positions: list[Position]) -> list[PerceivedObject]:
        perceived_objects = []
        for position in positions:
            terrain = self._map.get_terrain_at_position(position)
            if not terrain:
                continue
            organism = self._state_service.get_organism_at_position(position)
            relative_positon = position - observer_position
            perceived_object = _tile_to_perceived_object(relative_positon, terrain, organism)
            perceived_objects.append(perceived_object)
        return perceived_objects


    def get_all_renderable(self) -> Iterable[Renderable]:
        tiles = self._map.get_all_renderable()
        organisms = self._state_service.get_all_renderable()
        return chain(tiles,organisms)


    def _register_handlers(self):
        self._event_bus.on_command("change_state_requested", self._handle_state_change)
        self._event_bus.on_async("position_changed", self._on_position_changed)

    async def _notify_position_changed(self):
        await self._event_bus.emit("position update", {})


    async def _on_position_changed(self, payload: dict):
        organism_id = payload["organism_id"]
        position = payload["position"]
        self.update_position(organism_id, position)
        await self._notify_position_changed()


    async def _handle_state_change(self, payload, future):
        organism = payload["organism"]
        target_position = payload["target_position"]
        new_state = payload["new_state"]

        result = self._validate_position(target_position, organism.allowed_terrains)
        if result != MoveResult.SUCCESS:
            future.set_result(result)
            return

        self.update_position(organism.id, target_position)

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



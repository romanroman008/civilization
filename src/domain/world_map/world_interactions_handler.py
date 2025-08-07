from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.organism_id import OrganismID
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult

from domain.world_map.world_interactions_validator import WorldInteractionsValidator
from domain.world_map.world_map import WorldMap
from domain.world_map.world_state_service import WorldStateService


class WorldInteractionsHandler:
    def __init__(self,
                 world_map: WorldMap,
                 world_state_service: WorldStateService,
                 world_interactions_validator: WorldInteractionsValidator,
                 event_bus: EventBus):
        self._world_map = world_map
        self._world_state_service = world_state_service
        self._event_bus = event_bus
        self.world_interactions_validator = world_interactions_validator
        self._register_handlers()

    def _register_handlers(self):
        self._event_bus.on_command("change_state_requested", self._handle_state_change)
        self._event_bus.on_async("position_changed", self._on_position_changed)
        self._event_bus.on_command("kill_request", self._on_kill_request)

    def _create_world_interactions_validator(self):
        return WorldInteractionsValidator(world_map=self._world_map,
                                          world_state_service=self._world_state_service)

    async def _on_kill_request(self, payload: dict, future):
        killer_id = payload["killer_id"]
        victim_id = payload["victim_id"]

        if self.world_interactions_validator.is_kill_allowed(killer_id, victim_id):
            await self._notify_organism_death(victim_id)
            future.set_result(True)
        else:
            future.set_result(False)


    async def _notify_organism_death(self, organism_id: OrganismID):
        await self._event_bus.emit("death", {"organism_id": organism_id})


    async def _notify_position_changed(self):
        await self._event_bus.emit("position update", {})


    async def _on_position_changed(self, payload: dict):
        organism_id = payload["organism_id"]
        position = payload["position"]
        self._world_state_service.update_position(organism_id, position)
        await self._notify_position_changed()


    async def _handle_state_change(self, payload, future):
        organism = payload["organism"]
        target_position = payload["target_position"]

        result = self._validate_position(target_position, organism.allowed_terrains)
        if result != MoveResult.SUCCESS:
            future.set_result(result)
            return

        # self._world_state_service.update_position(organism.id, target_position)

        await self._event_bus.emit("organism_moved", {
            "organism" : organism,
            "position" : target_position,
        })

        future.set_result(MoveResult.SUCCESS)

    def _validate_position(self, position: Position, terrains: set[Terrain]) -> MoveResult:
        if not self._world_map.is_position_allowed(position, terrains):
            return MoveResult.OUT_OF_BOUNDS
        if self._world_state_service.is_occupied(position):
            return MoveResult.OCCUPIED
        if self._world_state_service.is_reserved(position):
            return MoveResult.RESERVED
        else:
            return MoveResult.SUCCESS
from typing import TYPE_CHECKING

from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.transform.transform_readonly import TransformReadOnly

if TYPE_CHECKING:
    from domain.organism.brain.brain import Brain
from domain.organism.perception.field_of_view import FieldOfView


from domain.organism.organism_id import OrganismID
from domain.services.event_bus import EventBus



class BrainInteractionsHandler:
    def __init__(self,
                 owner_id: OrganismID,
                 brain:"Brain",
                 transform_readonly:TransformReadOnly,
                 field_of_view: FieldOfView,
                 event_bus: EventBus):
        self._owner_id = owner_id
        self._brain = brain
        self._transform_readonly = transform_readonly
        self._field_of_view = field_of_view
        self._event_bus = event_bus
        self._register_handlers()

    def _register_handlers(self):
        self._event_bus.on_async("position update", self.update_field_view)
        self._event_bus.on_async("death", self.register_organism_death)

    async def update_field_view(self, payload):
        self._field_of_view.update(self._transform_readonly.position)

    async def register_organism_death(self, payload):
        organism_id = payload["organism_id"]
        if organism_id == self._owner_id:
            self._brain.kill_itself()


    async def notify_position_change(self):
        payload = {
            "organism_id": self._owner_id,
            "position": self._transform_readonly.position
        }
        await self._event_bus.emit_async("position_changed", payload)

    async def emit_kill_decision(self, target_id: OrganismID) -> bool:
        return await self._event_bus.emit_with_response("kill_request", {
            "killer_id": self._owner_id,
            "victim_id": target_id
        })



    async def emit_walking_decision(self, move_direction: Direction):
        target_position = self._direction_to_position(move_direction)

        result = await self._event_bus.emit_with_response("walk_request",{
            "organism_id": self._owner_id,
            "target_position": target_position
        })
        return result



    def _direction_to_position(self, direction: Direction) -> Position:
        return direction.vector() + self._transform_readonly.position
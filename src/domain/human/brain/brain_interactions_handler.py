from typing import TYPE_CHECKING

from domain.components.direction import Direction
from domain.components.position import Position
if TYPE_CHECKING:
    from domain.human.brain.brain import Brain
from domain.human.field_of_view import FieldOfView
from domain.human.vitals import Vitals
from domain.organism.instances.organism import Organism
from domain.organism.movement import Movement
from domain.organism.organism_id import OrganismID
from domain.services.event_bus import EventBus



class BrainInteractionsHandler:
    def __init__(self,
                 organism: Organism,
                 brain:"Brain",
                 field_of_view: FieldOfView,
                 vitals: Vitals,
                 movement: Movement,
                 event_bus: EventBus):
        self._organism = organism
        self._brain = brain
        self._field_of_view = field_of_view
        self._vitals = vitals
        self._movement = movement
        self._event_bus = event_bus
        self._register_handlers()

    def _register_handlers(self):
        self._event_bus.on_async("position update", self.update_field_view)
        self._event_bus.on_async("death", self.register_organism_death)

    async def update_field_view(self, payload):
        self._field_of_view.update(self._organism.position)

    async def register_organism_death(self, payload):
        organism_id = payload["organism_id"]
        if organism_id == self._organism.id:
            self._brain.kill_itself()


    async def notify_position_change(self):
        payload = {
            "organism": self._organism,
            "position": self._organism.position
        }
        await self._event_bus.emit_async("position_changed", payload)

    async def emit_kill_decision(self, target_id: OrganismID):
        result = await self._event_bus.emit("kill_request", {
            "killer_id": self._organism.id,
            "victim_id": target_id
        })


    async def emit_walking_decision(self, move_direction: Direction):
        target_position = self._direction_to_position(move_direction)

        result = await self._event_bus.emit_with_response("walk_request",{
            "organism": self._organism,
            "target_position": target_position
        })
        return result



    def _direction_to_position(self, direction: Direction) -> Position:
        return direction.vector() + self._organism.position
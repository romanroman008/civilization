from itertools import count
from typing import TYPE_CHECKING

from domain.components.position import Position
if TYPE_CHECKING:
    from domain.human.brain.brain import Brain
from domain.organism.instances.organism import Organism

from domain.organism.movement import Movement
from domain.organism.organism_id import OrganismID

from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.organism.state.idle_state import IdleState
from domain.organism.state.organism_state import OrganismState
from domain.world_map.position_validator_protocol import PositionValidatorProtocol


class Animal(Organism):
    _id_counter = count(1)
    def __init__(self,
                 prefab: OrganismPrefab,
                 position: Position,
                 brain: "Brain",
                 movement: Movement,
                 position_validator: PositionValidatorProtocol):
        super().__init__(prefab, position)
        self._id = OrganismID("animal", next(self._id_counter))
        self._movement = movement
        self._brain = brain
        self._position_validator = position_validator
        self._state = IdleState()

    @property
    def id(self) -> OrganismID:
        return self._id

    @property
    def is_moving(self) -> bool:
        return self._movement.is_moving

    @property
    def offset(self) -> tuple[int, int]:
        return self._offset_x, self._offset_y

    @property
    def target_position(self) -> Position:
        return self._movement.target_position

    async def set_state(self, state: OrganismState):
        if isinstance(self._state, type(state)):
            return
        await self._state.on_exit(self)

        self._state = state
        await self._state.on_enter(self)

    def connect(self):
        self._brain.set_animal(self)
        self._movement.set_animal(self)



    @property
    def is_alive(self) -> bool:
        return self._brain.is_alive


    def _rotate(self, angle: int, caller: Movement):
        if caller != self._movement:
            raise PermissionError("Only the registered Movement component can rotate this organism")
        self._rotation += angle

    def _move_offset(self, dx: int, dy: int, caller: Movement):
        if caller != self._movement:
            raise PermissionError("Only the registered Movement component can change offset of this organism")
        self._offset_x += dx
        self._offset_y += dy

    def _reset_offset(self, caller: Movement):
        if caller != self._movement:
            raise PermissionError("Only the registered Movement component can reset offset of this organism")
        self._offset_x = 0
        self._offset_y = 0

    def _reset_rotation(self, caller: Movement):
        if caller != self._movement:
            raise PermissionError("Only the registered Movement component can reset rotation of this organism")
        self._rotation = 0


    def _change_positon(self, position: Position, caller: Movement):
        if caller != self._movement:
            raise PermissionError("Only the registered Movement component can change position of this organism")

        if not self._position_validator.is_position_allowed(position, self._prefab.allowed_terrains):
            raise ValueError(f"Postion is {position} is not allowed")

        self._position = position

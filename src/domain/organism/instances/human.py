from itertools import count

from domain.components.position import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.human.brain.brain import Brain
from domain.human.field_of_view import FieldOfView

from domain.organism.human_movement import HumanMovement
from domain.organism.instances.organism import Organism
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.organism.state.human_state import HumanState
from domain.organism.state.idle_state import IdleState


class Human(Organism):
    _human_counter = count(1)

    def __init__(self, prefab: OrganismPrefab,  brain: "Brain", movement: HumanMovement):
        self._id = next(self._human_counter)
        self._prefab = prefab
        self._movement = movement
        self._brain = brain
        self._brain.set_human(self)
        self._state: HumanState = IdleState()


    @property
    def id(self) -> int:
        return self._id

    @property
    def sprite_key(self) -> str:
        return self._prefab.name

    @property
    def allowed_terrains(self):
        return self._prefab.allowed_terrains

    @property
    def is_moving(self) -> bool:
        return self._movement.is_moving


    @property
    def position(self) -> Position:
        return self._movement.position

    @property
    def rotation(self) -> int:
        return self._movement.rotation

    @property
    def offset(self) -> tuple[int, int]:
        return self._movement.offset_x, self._movement.offset_y

    @property
    def target_position(self) -> Position:
        return self._movement.target_position

    async def set_state(self, state: HumanState):
        if isinstance(self._state, type(state)):
            return
        await self._state.on_exit(self)

        self._state = state
        await self._state.on_enter(self)

    def __call__(self, *args, **kwargs):
        self._brain.tick(self.position)

    @property
    def brain(self):
        return self._brain

    @property
    def movement(self) -> HumanMovement:
        return self._movement

    @property
    def state(self):
        return self._state
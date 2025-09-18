from itertools import count
from typing import TYPE_CHECKING

from domain.components.position import Position
from domain.organism.movement.movement import Movement
from domain.organism.transform.transform import Transform

if TYPE_CHECKING:
    from domain.organism.brain.brain import Brain
from domain.organism.instances.organism import Organism


from domain.organism.organism_id import OrganismID

from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.organism.state.idle_state import IdleState



def normalize_angle(angle) -> int:
    angle = int(round(angle))
    r = (angle + 180) % 360 - 180
    return 180 if r == -180 else r


class Animal(Organism):
    _id_counter = count(1)
    def __init__(self,
                 prefab: OrganismPrefab,
                 position: Position,
                 brain: "Brain",
                 transform: Transform):
        super().__init__(prefab, position, transform)
        self._id = OrganismID(prefab.name, next(self._id_counter))
        self._brain = brain
        self._state = IdleState()
        self._set_transform_finalize()

    def _set_transform_finalize(self):
        self._transform.set_change_position_callback(self._change_position)

    @property
    def id(self) -> OrganismID:
        return self._id

    @property
    def is_alive(self) -> bool:
        return self._brain.is_alive

    def tick(self, tick: int):
        self._brain.tick(tick)

    def _change_position(self, target_position: Position):
        self._position = target_position



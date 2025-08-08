
from itertools import count

from domain.components.position import Position
from typing import TYPE_CHECKING

from domain.organism.instances.animal import Animal
from domain.organism.movement import Movement
from domain.organism.organism_id import OrganismID

if TYPE_CHECKING:
    from domain.human.brain.brain import Brain

from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Human(Animal):
    _human_counter = count(1)
    def __init__(self, prefab: OrganismPrefab, position: Position, brain: "Brain", movement: Movement):
        super().__init__(prefab, position, brain, movement)
        self._id = OrganismID("human", next(self._human_counter))


    @property
    def brain(self) -> "Brain":
        return self._brain

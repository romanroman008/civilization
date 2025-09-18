
from itertools import count

from domain.components.position import Position
from typing import TYPE_CHECKING

from domain.organism.instances.animal import Animal


from domain.organism.organism_id import OrganismID
from domain.organism.transform.transform import Transform

if TYPE_CHECKING:
    from domain.organism.brain.brain import Brain

from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Human(Animal):
    _human_counter = count(1)
    def __init__(self,
                 prefab: OrganismPrefab,
                 position: Position,
                 brain: "Brain",
                 transform: Transform):
        super().__init__(prefab, position, brain, transform)
        self._id = OrganismID(prefab.name, next(self._human_counter))


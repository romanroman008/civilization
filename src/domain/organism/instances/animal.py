from itertools import count
from typing import Callable

from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.instances.organism import Organism
from domain.organism.animal_movement import AnimalMovement
from domain.organism.organism_id import OrganismID

from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Animal(Organism):
    _id_counter = count(1)
    def __init__(self, prefab: OrganismPrefab, position: Position):
        self._id = OrganismID("animal", next(self._id_counter))
        self._prefab = prefab
        self._movement = AnimalMovement(position)



    def add_finalized_move(self, on_finalized_move: Callable[[Position, Position], None]):
        self._movement.add_finalized_move(on_finalized_move)

    def move(self, direction: Direction, distance: int = 1):
        self._movement.start_move(direction, distance, self._movement.position)

    def __call__(self, *args, **kwargs):
        self._movement.tick()
        #print(f"Animal {self.id} tick")

    @property
    def id(self) -> OrganismID:
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
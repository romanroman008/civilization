from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.instances.organism import Organism
from domain.organism.movement import Movement

from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Animal(Organism):
    def __init__(self, prefab: OrganismPrefab, position: Position):
        super().__init__(prefab, position)
        self._movement = Movement(position)

    def move(self, direction: Direction, distance: int = 1):
        self._movement.start_move(direction, distance, self._movement.position)

    def __call__(self, *args, **kwargs):
        self._movement.tick()

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
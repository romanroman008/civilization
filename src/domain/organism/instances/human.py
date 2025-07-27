from typing import Callable

from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.human_movement import HumanMovement
from domain.organism.instances.organism import Organism
from domain.organism.prefabs.organism_prefab import OrganismPrefab


class Human(Organism):
    def __init__(self, prefab: OrganismPrefab, position: Position):
        super().__init__(prefab, position)
        self._movement = HumanMovement(position)

    def add_finalized_move(self, on_finalized_move: Callable[[Position, Position], None]):
        self._movement.add_finalized_move(on_finalized_move)

    def move(self, direction: Direction, distance: int = 1):
        self._movement.start_move(direction, distance)

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

    @property
    def target_position(self) -> Position:
        return self._movement.target_position
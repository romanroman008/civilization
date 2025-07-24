from typing import Callable, Optional

from domain.components.direction import Direction
from domain.components.position import Position

import math

from domain.services.movement.movement_system import find_target_position


class HumanMovement:
    def __init__(self, position: Position, direction: Direction = Direction.BOT):
        self._position = position
        self._target_position = position

        self._rotation = 0
        self._target_rotation = 0
        self._rotation_step = 1

        self._direction = direction
        self._target_direction = direction

        self._offset_step = 1
        self._offset_x = 0
        self._target_offset_x = 0
        self._offset_step_x = 0

        self._offset_y = 0
        self._target_offset_y = 0
        self._offset_step_y = 0

        self._is_moving = False
        self.on_finalized_move: Optional[Callable[[Position, Position], None]] = None

    def add_finalized_move(self, finalized_move: Callable[[Position,Position], None]):
        self.on_finalized_move = finalized_move

    def start_move(self, direction: Direction, distance: int, position: Position):
        self._is_moving = True
        self._target_direction = direction
        self._target_position = find_target_position(position, direction, distance)

        self._target_offset_x = direction.vector().x * distance * 100
        self._offset_step_x = int(math.copysign(self._offset_step, self._target_offset_x))

        self._target_offset_y = direction.vector().y * distance * 100
        self._offset_step_y = int(math.copysign(self._offset_step, self._target_offset_y))

    def tick(self):
        if not self.is_moving:
            return

        if not self._is_offset_at_target():
            self._move_offset()
            return

        self._finalize_movement()

    def _move_offset(self):
        if not self._is_x_offset_at_target():
            self._offset_x += self._offset_step_x
        if not self._is_y_offset_at_target():
            self._offset_y += self._offset_step_y

    def _is_offset_at_target(self) -> bool:
        return self._offset_x == self._target_offset_x and self._offset_y == self._target_offset_y

    def _is_x_offset_at_target(self) -> bool:
        return self._offset_x == self._target_offset_x

    def _is_y_offset_at_target(self) -> bool:
        return self._offset_y == self._target_offset_y

    def _finalize_movement(self):
        self.on_finalized_move(self._position, self._target_position)
        self._position = self._target_position
        self._offset_x = 0
        self._offset_y = 0
        self._target_offset_x = 0
        self._target_offset_y = 0
        self._is_moving = False


    @property
    def position(self) -> Position:
        return self._position

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def offset_x(self) -> int:
        return self._offset_x

    @property
    def offset_y(self) -> int:
        return self._offset_y

    @property
    def rotation(self) -> int:
        return self._rotation

    @property
    def is_moving(self) -> bool:
        return self._is_moving

    @property
    def target_position(self) -> Position:
        return self._target_position
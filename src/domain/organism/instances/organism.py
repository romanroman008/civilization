import math
from typing import Optional

from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.services.movement.movement_system import find_needed_direction, find_target_position, find_shortest_rotation


class Organism:

    def __init__(self, prefab: OrganismPrefab, position):
        self._prefab = prefab
        self._position = position
        self._target_position = position

        self._rotation = 0
        self._target_rotation = 0
        self._rotation_step = 1

        self._direction = Direction.BOT
        self._target_direction = self._direction

        self._offset_step = 1

        self._offset_x = 0
        self._target_offset_x = self._offset_x
        self._offset_step_x = self._offset_step

        self._offset_y = 0
        self._target_offset_y = self._offset_y
        self._offset_step_y = self._offset_step

        self._is_moving = False

    @property
    def sprite_key(self) -> str:
        return self._prefab.name

    @property
    def block_radius(self) -> int:
        return self._prefab.block_radius

    @property
    def position(self) -> Position:
        return self._position

    @property
    def rotation(self) -> float:
        return self._rotation

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def offset_x(self) -> float:
        return self._offset_x

    @property
    def offset_y(self) -> float:
        return self._offset_y

    @property
    def is_moving(self) -> bool:
        return self._is_moving


    def move(self, direction: Direction, distance):
        self._is_moving = True
        self._target_direction = direction
        self._target_position = find_target_position(self.position, direction, distance)

        self._target_rotation = find_shortest_rotation(self._direction, direction)
        self._rotation_step = int(math.copysign(self._rotation_step, self._target_rotation))

        self._target_offset_x = direction.vector().x * distance * 100
        self._offset_step_x = int(math.copysign(self._offset_step, self._target_offset_x))
        self._target_offset_y = direction.vector().y * distance * 100
        self._offset_step_y = int(math.copysign(0.1, self._target_offset_y))


    def _rotate(self):
        self._rotation = (self._rotation + self._rotation_step + 180) % 360 - 180

        direction_by_angle = {
            0: Direction.BOT,
            90: Direction.LEFT,
            -180: Direction.TOP,
            -90: Direction.RIGHT,
        }
        if self._rotation in direction_by_angle:
            self._facing = direction_by_angle[self._rotation]

    def _move_offset(self):
        if not self._is_x_offset_at_target():
            self._move_offset_x(self._offset_step_x)
        if not self._is_y_offset_at_target():
            self._move_offset_y(self._offset_step_y)


    def _move_offset_x(self, x:int):
        self._offset_x += x

    def _move_offset_y(self, y:int):
        self._offset_y += y

    def _is_facing_target(self) -> bool:
        return self._direction != self._target_direction

    def _is_offset_at_target(self) -> bool:
        return self._is_x_offset_at_target() and self._is_y_offset_at_target()

    def _is_x_offset_at_target(self) -> bool:
        return self._offset_x == self._target_offset_x

    def _is_y_offset_at_target(self) -> bool:
        return self._offset_y == self._target_offset_y

    def _reset_offset(self):
        self._offset_x = 0
        self._offset_y = 0
        self._target_offset_x = self._offset_x
        self._target_offset_y = self._offset_y

    def _finalize_movement(self):
        self._position = self._target_position
        self._reset_offset()
        self._is_moving = False



    def __call__(self, *args, **kwargs):
        if not self.is_moving:
            return

        if not self._is_facing_target():
            self._rotate()
            return

        if not self._is_offset_at_target():
            self._move_offset()
            return

        self._finalize_movement()











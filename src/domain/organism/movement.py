import asyncio
from abc import abstractmethod, ABC

from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.movement_utils import find_divisors, quantize_to_set, find_shortest_rotation, find_target_position
from shared.config import CONFIG

from shared.constans import OFFSET_NORMALIZED_RANGE, ROTATION_SPEED_DELAY_PER_STEP, MOVEMENT_SPEED_DELAY_PER_STEP


class Movement(ABC):
    def __init__(self, position: Position, direction: Direction = Direction.BOT):
        self._position = position
        self._target_position = position

        self._rotation = 0
        self._offset_x = 0
        self._offset_y = 0

        self._rotation_step = 1
        self._offset_step = 1

        self._direction = direction
        self._target_direction = direction

        self._is_moving = False

        self._prepare_the_necessary_values(CONFIG["movement_speed"], CONFIG["movement_rotation_speed"])

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


    def _prepare_the_necessary_values(self, movement_speed:int, movement_rotation_speed:int):
        allowed_speed_values = find_divisors(OFFSET_NORMALIZED_RANGE)
        allowed_rotation_speed_values = find_divisors(Direction.min_rotation_degrees())
        self._offset_step = quantize_to_set(movement_speed, allowed_speed_values)
        self._rotation_step = quantize_to_set(movement_rotation_speed, allowed_rotation_speed_values)

    def _prepare_to_move(self, target_direction: Direction):
        self._is_moving = True
        self._target_position = find_target_position(self._target_position, self._direction)
        self._target_direction = target_direction

    def _finalize_move(self):
        self._position = self._target_position
        self._offset_x = 0
        self._offset_y = 0
        self._is_moving = False
        self._direction = self._target_direction

    @abstractmethod
    async def move_to(self, target_direction: Direction):
        ...

    async def rotate(self):
        target_rotation = find_shortest_rotation(self._direction, self._target_direction)
        total_rotation_steps = target_rotation // self._rotation_step

        for _ in range(total_rotation_steps):
            self._rotation += self._rotation_step
            await asyncio.sleep(ROTATION_SPEED_DELAY_PER_STEP)

    async def move_offset(self):
        x_done, y_done = False, False
        dx = self._target_direction.vector().x * self._offset_step
        dy = self._target_direction.vector().y * self._offset_step

        total_offset_x_steps = dx // self._offset_step
        total_offset_y_steps = dy // self._offset_step

        offset_steps = max(total_offset_x_steps, total_offset_y_steps)

        for _ in range(offset_steps):
            if not x_done:
                self._offset_x += dx
            if not y_done:
                self._offset_y += dy
            await asyncio.sleep(MOVEMENT_SPEED_DELAY_PER_STEP)






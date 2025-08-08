import asyncio
import logging
import math
from abc import abstractmethod, ABC
from typing import Optional, TYPE_CHECKING

from domain.components.direction import Direction
from domain.components.position import Position
from shared.logger import get_logger

if TYPE_CHECKING:
    from domain.organism.instances.animal import Animal
from domain.organism.movement_utils import find_divisors, quantize_to_set, find_shortest_rotation, find_target_position

from shared.config import CONFIG

from shared.constans import OFFSET_NORMALIZED_RANGE, ROTATION_SPEED_DELAY_PER_STEP, MOVEMENT_SPEED_DELAY_PER_STEP


class Movement(ABC):
    def __init__(self, direction: Direction = Direction.BOT):
        self._animal: Optional[Animal] = None
        self._target_position: Optional[Position] = None

        self._direction = direction
        self._target_direction = direction

        self._is_moving = False

        self._prepare_the_necessary_values(CONFIG["movement_speed"], CONFIG["movement_rotation_speed"])

        self._logger = get_logger(f"Movement: ", level=logging.INFO, log_filename="movement.log")

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def is_moving(self) -> bool:
        return self._is_moving

    @property
    def target_position(self) -> Position:
        return self._target_position

    def set_animal(self, animal:"Animal"):
        if self._animal is not None:
            raise RuntimeError(f"The animal is already set.")
        self._animal = animal
        self._target_position = animal.position


    def _prepare_the_necessary_values(self, movement_speed:int, movement_rotation_speed:int):
        allowed_speed_values = find_divisors(OFFSET_NORMALIZED_RANGE)
        allowed_rotation_speed_values = find_divisors(Direction.min_rotation_degrees())
        self._offset_step = quantize_to_set(movement_speed, allowed_speed_values)
        self._rotation_step = quantize_to_set(movement_rotation_speed, allowed_rotation_speed_values)

    def _prepare_to_move(self, target_direction: Direction):
        self._is_moving = True
        self._target_position = find_target_position(self._target_position, target_direction)
        self._target_direction = target_direction

    def _finalize_move(self):
        self._animal._change_positon(self._target_position, self)
        self._animal._reset_offset(self)
        self._is_moving = False


    @abstractmethod
    async def move_to(self, target_direction: Direction):
        ...

    async def _rotate(self):

        target_rotation = find_shortest_rotation(self._direction, self._target_direction)
        total_rotation_steps = abs(target_rotation // self._rotation_step)


        for _ in range(total_rotation_steps):
            self._animal._rotate(self._rotation_step * math.copysign(1, target_rotation), self)
            await asyncio.sleep(ROTATION_SPEED_DELAY_PER_STEP)

        self._direction = self._target_direction

    async def _move_offset(self):
        dx = self._target_direction.vector().x * self._offset_step * 100
        dy = self._target_direction.vector().y * self._offset_step * 100

        total_offset_x_steps = abs(dx // self._offset_step)
        total_offset_y_steps = abs(dy // self._offset_step)


        offset_steps = max(total_offset_x_steps, total_offset_y_steps)


        for _ in range(offset_steps):
            offset_x, offset_y = self._animal.offset
            if offset_x != dx:
                self._animal._move_offset(self._offset_step * math.copysign(1,dx),0, self)
            if offset_y != dy:
                self._animal._move_offset(0,self._offset_step * math.copysign(1,dy), self)
            await asyncio.sleep(MOVEMENT_SPEED_DELAY_PER_STEP)






    async def log(self, target_rotation: int):
        self._logger.info(f"Actual direction: {self.direction} to {self._target_direction}")
        self._logger.info(f"Actual rotation: {self._animal.rotation} to {target_rotation}")




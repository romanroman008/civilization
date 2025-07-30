import asyncio

from domain.components.direction import Direction
from domain.components.position import Position
from domain.services.movement.movement_system import find_target_position


class HumanMovement:
    def __init__(self, position: Position, direction: Direction = Direction.BOT):
        self._position = position
        self._target_position = position
        self._direction = direction
        self._offset_x = 0
        self._offset_y = 0
        self._rotation = 0
        self._is_moving = False

    async def move_to(self, direction: Direction, distance: int = 1):
        if self._is_moving:
            return

        self._is_moving = True
        self._direction = direction
        self._target_position = find_target_position(self._position, direction, distance)

        total_steps = distance * 100
        step = 1
        dx = direction.vector().x * step
        dy = direction.vector().y * step

        for _ in range(total_steps):
            self._offset_x += dx
            self._offset_y += dy
            await asyncio.sleep(0.016)  # ~60 FPS

        # Finalize move
        self._position = self._target_position
        self._offset_x = 0
        self._offset_y = 0
        self._is_moving = False

    @property
    def position(self) -> Position:
        return self._position

    @property
    def offset_x(self) -> int:
        return self._offset_x

    @property
    def offset_y(self) -> int:
        return self._offset_y

    @property
    def is_moving(self) -> bool:
        return self._is_moving

    @property
    def rotation(self):
        return self._rotation

    @property
    def target_position(self) -> Position:
        return self._target_position


from domain.components.direction import Direction
from domain.organism.movement import Movement
from shared.config import CONFIG


class HumanMovement(Movement):
    def __init__(self, direction: Direction = Direction.BOT):
        super().__init__(direction)
        self._prepare_the_necessary_values(CONFIG["movement_speed"], CONFIG["movement_rotation_speed"])

    async def move_to(self, target_direction: Direction):
        if self._is_moving:
            return

        self._prepare_to_move(target_direction)

        await self._move_offset()

        self._finalize_move()

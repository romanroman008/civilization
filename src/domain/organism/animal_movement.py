
from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.movement import Movement

from shared.config import CONFIG




class AnimalMovement(Movement):
    def __init__(self, position: Position, direction: Direction = Direction.BOT):
        super().__init__(position, direction)
        self._prepare_the_necessary_values(CONFIG["movement_speed"], CONFIG["movement_rotation_speed"])


    async def move_to(self, target_direction: Direction):
        if self._is_moving:
            return

        self._prepare_to_move(target_direction)

        await self.rotate()
        await self.move_offset()

        self._finalize_move()








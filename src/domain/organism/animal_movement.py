from domain.components.direction import Direction


from domain.organism.movement import Movement
from domain.world_map.position_validator_protocol import PositionValidatorProtocol

from shared.config import CONFIG


class AnimalMovement(Movement):
    def __init__(self, position_validator: PositionValidatorProtocol,
                 direction: Direction = Direction.BOT):
        super().__init__(direction)
        self._position_validator = position_validator
        self._prepare_the_necessary_values(CONFIG["movement_speed"], CONFIG["movement_rotation_speed"])

    async def move_to(self, target_direction: Direction):
        if (
                self._is_moving or
                self._position_validator.is_position_allowed(self.target_position,self._animal.allowed_terrains)):
            return

        self._prepare_to_move(target_direction)

        await self._rotate()
        await self._move_offset()

        self._finalize_move()

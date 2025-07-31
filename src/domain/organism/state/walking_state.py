from domain.components.direction import Direction
from domain.organism.instances.human import Human
from domain.organism.state.human_state import HumanState
from domain.organism.state.idle_state import IdleState


class WalkingState(HumanState):
    def __init__(self, direction: Direction):
        super().__init__()
        self.direction = direction

    async def on_enter(self, human: Human):
        if not self._is_busy:
            self._logger.info(f"Human {human.id} has started walking")
            self._is_busy = True

            await human.movement.move_to(self.direction, 1)

            await human.set_state(IdleState())



    async def on_exit(self, human: Human):
        self._logger.info(f"Human {human.id} has stopped walking")
        self._is_busy = False

    async def on_tick(self, human: Human):
        pass

from domain.components.direction import Direction
from domain.organism.instances.human import Human
from domain.organism.state.human_state import HumanState
from domain.organism.state.idle_state import IdleState


class WalkingState(HumanState):
    def __init__(self):
        super().__init__()

    async def on_enter(self, human: Human):
        self._is_busy = True
        self._logger.info(f"Human {human.id} has started walking")




    async def on_exit(self, human: Human):
        self._is_busy = False
        self._logger.info(f"Human {human.id} has stopped walking")


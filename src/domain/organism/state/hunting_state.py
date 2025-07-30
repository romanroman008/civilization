from domain.components.direction import Direction

from domain.organism.instances.human import Human
from domain.organism.state.human_state import HumanState



class HuntingState(HumanState):
    def __init__(self, path: list[Direction]):
        self._path: list[Direction] = path

    async def on_enter(self, human: Human):
        self.logger.info(f"Human {human.id} has started hunting")

        for direction in self._path:
            await human.movement.move_to(direction)




    async def on_exit(self, human: Human):
        self.logger.info(f"Human {human.id} has stopped hunting")



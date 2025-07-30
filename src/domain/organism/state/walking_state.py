from domain.components.direction import Direction
from domain.organism.instances.human import Human
from domain.organism.state.human_state import HumanState
from domain.organism.state.idle_state import IdleState


class WalkingState(HumanState):
    def __init__(self, direction: Direction):
        self.direction = direction

    async def on_enter(self, human: Human):
        self.logger.info(f"Human {human.id} has started walking")

        await human.movement.move_to(self.direction, 1)

        await human.set_state(IdleState())



    async def on_exit(self, human: Human):
        self.logger.info(f"Human {human.id} has stopped walking")

    async def on_tick(self, human: Human):
        pass

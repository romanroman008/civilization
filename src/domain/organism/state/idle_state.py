from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.organism.instances.human import Human

from domain.organism.state.human_state import HumanState


class IdleState(HumanState):
    async def on_enter(self,  human: "Human"):
        self._logger.info(f"Human {human.id} is idle now")

    async def on_exit(self,  human: "Human"):
        self._logger.info(f"Human {human.id} has stopped being idle")

    async def on_tick(self,  human: "Human"):
        pass

from domain.components.direction import Direction
from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism

from domain.organism.state.organism_state import OrganismState
from domain.organism.state.idle_state import IdleState


class WalkingState(OrganismState):
    def __init__(self):
        super().__init__()

    async def on_enter(self, organism: Organism):
        self._is_busy = True
        self._logger.info(f"Human {organism.id} has started walking")


    async def on_exit(self, organism: Organism):
        self._is_busy = False
        self._logger.info(f"Human {organism.id} has stopped walking")


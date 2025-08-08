

from domain.organism.instances.organism import Organism



from domain.organism.state.organism_state import OrganismState


class IdleState(OrganismState):
    async def on_enter(self, organism: Organism):
        self._is_busy = False
    #    self._logger.info(f"Human {organism.id} is idle now")

    async def on_exit(self, organism: Organism):
        pass
      #  self._logger.info(f"Human {organism.id} has stopped being idle")


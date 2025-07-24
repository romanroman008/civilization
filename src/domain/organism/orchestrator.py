from domain.organism.instances.organism import Organism


class Orchestrator:
    def __init__(self, organisms: list[Organism]):
        self._organisms = organisms


    def __call__(self, *args, **kwargs):
        for organism in self._organisms:
            organism()
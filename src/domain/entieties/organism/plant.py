from dataclasses import dataclass


from domain.entieties.organism.organism import Organism


@dataclass
class Plant(Organism):
    is_alive: bool = True



    def tick(self):
        ...


from dataclasses import dataclass

from domain.entieties.organism.organism import Organism


@dataclass
class Animal(Organism):
    is_alive: bool = True



    def tick(self):
        ...







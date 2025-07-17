from dataclasses import dataclass


from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position


@dataclass
class Plant(Organism):
    is_alive: bool = True



    def tick(self):
        ...


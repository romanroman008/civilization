from dataclasses import dataclass

from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


@dataclass
class Animal(Organism):
    is_alive: bool = True



    def tick(self):
        ...







from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


class Animal(Organism):
    def __init__(self, name:str, position:Position, allowed_terrains: set[Terrain], speed: int = 1):
        super().__init__(name, position, allowed_terrains)
        self.is_alive = True
        self.speed = speed

    def tick(self):
        pass







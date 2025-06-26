from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


class Plant(Organism):
    def __init__(self, name: str, position: Position, allowed_terrains: set[Terrain]):
        super().__init__(name, position, allowed_terrains)
        self.is_alive = True

    def tick(self):
        pass
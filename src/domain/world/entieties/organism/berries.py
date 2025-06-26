from domain.world.entieties.organism.plant import Plant
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


class Berries(Plant):
    def __init__(self, name: str, position: Position, allowed_terrains: set[Terrain] = None):
        if allowed_terrains is None:
            allowed_terrains = {Terrain.GRASS}
        super().__init__(name, position, allowed_terrains)


    def tick(self):
        pass

from abc import ABC, abstractmethod


from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


class Organism(ABC):
    def __init__(self, name, position: Position, allowed_terrain:set[Terrain]):
        self.name = name
        self.position = position
        self.allowed_terrains = allowed_terrain


    @abstractmethod
    def tick(self):
        pass


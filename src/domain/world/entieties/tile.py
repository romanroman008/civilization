

from dataclasses import dataclass, field
from typing import List
from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


@dataclass
class Tile:
    id: int
    x: int
    y: int
    terrain: Terrain
    organisms: List[Organism] = field(default_factory=list)
    isOccupied: bool = False

    def add_organism(self, organism: Organism):
        self.organisms.append(organism)
        self.isOccupied = True

    def remove_organism(self, organism: Organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            if not self.organisms:
                self.isOccupied = False

    @property
    def sprite_key(self) -> str:
        return self.terrain

    @property
    def position(self) -> Position:
        return Position(self.x, self.y)


from dataclasses import dataclass, field
from typing import List
from domain.entieties.organism.organism import Organism
from domain.components.position import Position
from domain.components.terrain import Terrain


@dataclass
class Tile:
    _id: int
    _x: int
    _y: int
    _terrain: Terrain
    _organisms: List[Organism] = field(default_factory=list)

    @property
    def id(self):
        return self._id

    @property
    def sprite_key(self):
        return self._terrain

    @property
    def terrain(self) -> str:
        return self._terrain

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def is_occupied(self):
        return bool(self._organisms)

    @property
    def position(self) -> Position:
        return Position(self.x, self.y)


    def add_organism(self, organism: Organism):
        self._organisms.append(organism)


    def remove_organism(self, organism: Organism):
        if organism in self._organisms:
            self._organisms.remove(organism)



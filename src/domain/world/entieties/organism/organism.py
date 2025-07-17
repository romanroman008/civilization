from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from domain.world.entieties.position import Position


@dataclass
class Organism(ABC):
    name: str
    allowed_terrains: set
    block_radius: int = 0
    _position: Optional[Position] = None

    @abstractmethod
    def tick(self):
        ...

    @property
    def sprite_key(self) -> str:
        return self.name

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position):
        self._position = value
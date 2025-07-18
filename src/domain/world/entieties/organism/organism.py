from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from domain.world.entieties.position import Position


@dataclass
class Organism(ABC):
    _name: str
    _allowed_terrains: set
    _block_radius: int = 0
    _position: Optional[Position] = None

    @abstractmethod
    def tick(self):
        ...

    @property
    def name(self) -> str:
        return self._name

    @property
    def allowed_terrains(self) -> set:
        return self._allowed_terrains

    @property
    def sprite_key(self) -> str:
        return self._name

    @property
    def block_radius(self) -> int:
        return self._block_radius

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position):
        self._position = value
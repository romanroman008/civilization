from typing import Protocol

from domain.components.position import Position
from domain.components.terrain import Terrain


class PositionValidatorProtocol(Protocol):
    def is_position_allowed(self, position: Position, allowed_terrains: set[Terrain]) -> bool: ...

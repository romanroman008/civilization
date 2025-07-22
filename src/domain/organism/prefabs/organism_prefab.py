from dataclasses import dataclass

from domain.components.direction import Direction
from domain.components.position import Position


@dataclass(frozen=True)
class OrganismPrefab:
    name: str
    allowed_terrains: set
    block_radius: int = 0




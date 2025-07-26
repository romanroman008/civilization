from dataclasses import dataclass
from typing import Optional

from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.instances.organism import Organism

@dataclass(frozen=True)
class PerceivedObject:
    relative_position: Position
    terrain: Terrain
    organism: Optional[Organism] = None
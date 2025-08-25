from dataclasses import dataclass
from typing import Optional

from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.perception.organism_info import OrganismInfo


@dataclass(frozen=True)
class PerceivedObject:
    relative_position: Position
    terrain: Terrain
    organism_info: Optional[OrganismInfo] = None
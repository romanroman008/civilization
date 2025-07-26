from dataclasses import dataclass

from domain.components.direction import Direction
from domain.human.perception.organism_info import OrganismInfo

@dataclass
class AnimalInfo(OrganismInfo):
    last_seen_direction: Direction
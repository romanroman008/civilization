from dataclasses import dataclass

from domain.human.perception.organism_info import OrganismInfo


@dataclass
class PlantInfo(OrganismInfo):
    is_edible: bool
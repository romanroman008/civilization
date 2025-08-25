from dataclasses import dataclass

from domain.organism.perception.organism_info import OrganismInfo


@dataclass
class PlantInfo(OrganismInfo):
    is_edible: bool
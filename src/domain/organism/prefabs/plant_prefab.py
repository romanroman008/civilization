from dataclasses import dataclass

from domain.organism.prefabs.organism_prefab import OrganismPrefab

@dataclass(frozen=True)
class PlantPrefab(OrganismPrefab):
    is_edible: bool
    block_radius: int = 0
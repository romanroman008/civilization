from dataclasses import dataclass

from domain.organism.prefabs.organism_prefab import OrganismPrefab


@dataclass(frozen=True)
class HumanPrefab(OrganismPrefab):
    pass
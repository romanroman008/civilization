from dataclasses import dataclass


@dataclass(frozen=True)
class OrganismPrefab:
    name: str
    allowed_terrains: set




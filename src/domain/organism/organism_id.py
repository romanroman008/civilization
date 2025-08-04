from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrganismID:
    kind: str
    id: int

import array
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrganismSoA:
    ids: array
    xs: array
    ys: array
    rots: array
    sprites: array
    alives: array
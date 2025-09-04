import array
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrganismSoA:
    ids: array
    xs: array
    ys: array
    offset_xs: array
    offset_ys: array
    rots: array
    sprites: array
    alives: array
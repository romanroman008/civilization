import array
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TileSoA:
    xs: array
    ys: array
    sprites: array

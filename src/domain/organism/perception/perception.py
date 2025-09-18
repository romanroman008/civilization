from dataclasses import dataclass
import array




@dataclass(frozen=True, slots=True)
class Perception:
    xs: array
    ys: array
    terrains: array
    organisms: array
    allowed: array
    organisms_id: array
    organisms_alive: array
    offsets_x: array
    offsets_y: array
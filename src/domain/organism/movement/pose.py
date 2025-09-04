from dataclasses import dataclass

from domain.components.direction import Direction


@dataclass(frozen=True, slots = True)
class Pose:
    direction: Direction
    rotation:float
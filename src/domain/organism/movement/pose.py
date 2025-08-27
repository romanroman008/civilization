from dataclasses import dataclass

@dataclass(frozen=True, slots = True)
class Pose:
    x:float
    y:float
    rotation:float
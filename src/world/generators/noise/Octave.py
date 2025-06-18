from dataclasses import dataclass


@dataclass(frozen=True)
class Octave:
    frequency: float
    amplitude: float
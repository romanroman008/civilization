from typing import Protocol


class NoiseGenerator(Protocol):
    def noise2(self, x: float, y: float) -> float:
        ...
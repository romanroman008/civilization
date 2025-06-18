from typing import List

from opensimplex import OpenSimplex

from tools.Utils import normalize_layered_noise
from world.generators.noise.NoiseGenerator import NoiseGenerator
from world.generators.noise.Octave import Octave


class OpenSimplexNoiseGenerator(NoiseGenerator):
    def __init__(self):
        self.__octaves: List[Octave] = []
        self.__seed = 1
        self.__noise = OpenSimplex(seed=self.__seed)


    def noise2(self, x: float, y: float) -> float:
        amplitudes_sum = 0
        noise_val = 0
        for octave in self.__octaves:
            noise_val += octave.amplitude * self.__noise.noise2(x * octave.frequency, y * octave.frequency)
            amplitudes_sum += octave.amplitude
        return normalize_layered_noise(noise_val, amplitudes_sum)


    def set_octaves(self, octaves: List[Octave]) -> None:
        if not octaves:
            raise ValueError("Octaves list cannot be empty.")
        for i, o in enumerate(octaves):
            if o.amplitude <= 0 or o.frequency <= 0:
                raise ValueError(f"Invalid octave at index {i}: amplitude and frequency must be > 0")
        self.__octaves = octaves


    def set_seed(self, seed: int):
        if not (0 <= seed <= 2 ** 63 - 1):
            raise ValueError(f"Seed {seed} out of valid range [0, 2^63 - 1]")
        self.__seed = seed
        self.__noise = OpenSimplex(seed=seed)



    @staticmethod
    def normalize_layered_noise(value: float, amplitudes_sum: float) -> float:
        avg = value / amplitudes_sum
        return (avg + 1) / 2
import json
from pathlib import Path
from typing import List, Callable, Union

from world.biome.Biome import Biome


class BiomeRepository:
    ID_OCEAN = "OCEAN"
    ID_UNKNOWN = "UNKNOWN"

    def __init__(self, biomes: List[Biome]):
        self.biomes = biomes

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "BiomeRepository":
        with open(Path(path), "r") as f:
            raw = json.load(f)
        biomes = [Biome(**{**b, "color": tuple(b.get("color", [0, 0, 0]))}) for b in raw]
        return cls(biomes)

    def _validate_required_biomes(self) -> None:
        required_ids = {self.ID_OCEAN, self.ID_UNKNOWN}
        existing_ids = {b.id for b in self.biomes}
        missing = required_ids - existing_ids
        if missing:
            raise ValueError(f"Missing required biome definitions: {missing}")


    def get_fallback_biome(self) -> Biome:
        return next((b for b in self.biomes if b.id == self.ID_UNKNOWN), self.biomes[0])

    def get_ocean_level(self) -> float:
        ocean = next(b for b in self.biomes if b.id == self.ID_OCEAN)
        return ocean.elevation_max

    def get_biomes_by_id(self, ids: List[str]) -> List[Biome]:
        return [b for b in self.biomes if b.id in ids]

    def find_biomes(self, predicate: Callable[[Biome], bool]) -> List[Biome]:
        return [b for b in self.biomes if predicate(b)]

    def get_all(self) -> List[Biome]:
        return self.biomes[:]



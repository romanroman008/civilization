import json
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Biome:
    id:str
    name:str
    latitude_min:float
    latitude_max:float
    elevation_min:float
    elevation_max:float
    temperature_min:float
    temperature_max:float
    moisture_min:float
    moisture_max:float
    color: Tuple[int, int, int] = (255, 255, 255)

    @staticmethod
    def load_from_json(path: str) -> List["Biome"]:
        with open(path, "r") as f:
            raw = json.load(f)
        biomes = []
        for b in raw:
            b["color"] = tuple(b.get("color", [0, 0, 0]))
            biomes.append(Biome(**b))
        return biomes



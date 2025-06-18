import json
from pathlib import Path
from typing import List, Union

from world.climate.ClimateZoneData import ClimateZoneData


class ClimateZoneRepository():
    def __init__(self, zones: List[ClimateZoneData]):
        self.zones = zones

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "ClimateZoneRepository":
        with open(Path(path), "r") as f:
            raw = json.load(f)
        zones = [ClimateZoneData(**z) for z in raw]
        return cls(zones)


    def get_all(self) -> List[ClimateZoneData]:
        return self.zones[:]

    def get_by_id(self, id: str) -> ClimateZoneData:
        for z in self.zones:
            if z.id == id:
                return z
        raise KeyError(f"No such zone: {id}")
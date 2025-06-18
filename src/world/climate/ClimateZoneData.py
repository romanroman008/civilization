from dataclasses import dataclass

from world.climate.ClimateZone import ClimateZone

@dataclass(frozen=True)
class ClimateZoneData:
    id: ClimateZone
    latitude_min: float
    latitude_max: float
from typing import Optional

from world.climate.ClimateClassifier import ClimateClassifier
from world.climate.ClimateZone import ClimateZone
from world.climate.ClimateZoneData import ClimateZoneData
from world.climate.ClimateZoneRepository import ClimateZoneRepository


class LatitudeBasedClimateClassifier(ClimateClassifier):
    def __init__(self, climate_zones_repository: ClimateZoneRepository):
        self.climate_zones = climate_zones_repository.get_all()

    def _find_matching_zone(self, latitude) -> Optional[ClimateZoneData]:
        for zone in self.climate_zones:
            if zone.latitude_min <= latitude <= zone.latitude_max:
                return zone
        return None


    def classify(self, latitude) -> ClimateZone:
        zone = self._find_matching_zone(latitude)
        if zone is None:
            raise ValueError(f"No climate zone matched latitude={latitude:.3f}")
        return zone.id
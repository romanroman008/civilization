from typing import Optional, List
from world.biome.Biome import Biome


class BiomeClassifier:
    def __init__(self, biomes: List[Biome]):
        self.biomes = biomes
        self.fallback_biome = next((b for b in self.biomes if b.id == "UNKNOWN"), None)

    def classify(
        self,
        latitude: float,
        temperature: float,
        elevation: float,
        moisture: float
    ) -> Optional[Biome]:
        candidates = []

        for biome in self.biomes:
            if (
                biome.temperature_min <= temperature <= biome.temperature_max and
                biome.elevation_min <= elevation <= biome.elevation_max and
                biome.moisture_min <= moisture <= biome.moisture_max
            ):
                # Jeśli latitude_min/latitude_max są dostępne w Biome, dodaj to:
                if hasattr(biome, "latitude_min") and hasattr(biome, "latitude_max"):
                    if not (biome.latitude_min <= latitude <= biome.latitude_max):
                        continue
                candidates.append(biome)

        if not candidates:
            return self.fallback_biome  # lub Unknown

        # Najlepiej dopasowany biom = najbardziej "specyficzny" (najwęższe zakresy)
        def specificity(b: Biome) -> float:
            return (
                (b.elevation_max - b.elevation_min) +
                (b.temperature_max - b.temperature_min) +
                (b.moisture_max - b.moisture_min)
            )

        return min(candidates, key=specificity)

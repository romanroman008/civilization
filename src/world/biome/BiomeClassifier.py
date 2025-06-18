from world.biome.Biome import Biome
from world.biome.BiomeRepository import BiomeRepository


class BiomeClassifier:
    def __init__(self, biome_repository: BiomeRepository):
        self.biome_repository = biome_repository

    def classify(self, latitude: float, temperature: float, elevation: float, moisture: float) -> Biome:
        # Krok 1 – Ocean
        if elevation <= self.biome_repository.get_ocean_level():
            return self.biome_repository.get_biomes_by_id([self.biome_repository.ID_OCEAN])[0]

        # Krok 2 – Dopasuj lądowe biomy wg podstawowych zakresów
        candidates = self.biome_repository.find_biomes(
            lambda b: (
                b.latitude_min <= latitude <= b.latitude_max and
                b.temperature_min <= temperature <= b.temperature_max and
                b.elevation_min <= elevation <= b.elevation_max
            )
        )

        if not candidates:
            return self.biome_repository.get_fallback_biome()

        # Wybierz najbardziej specyficzny biom (najwęższy zakres)
        def specificity(b: Biome) -> float:
            return (
                (b.latitude_max - b.latitude_min) +
                (b.temperature_max - b.temperature_min) +
                (b.elevation_max - b.elevation_min)
            )

        return min(candidates, key=specificity)

import random

from domain.world.entieties.organism.plant import Plant
from domain.world.entieties.position import Position
from domain.world.entieties.world_map import WorldMap


class PlantsGenerator:
    def __init__(self, count: int, species_distribution: dict[Plant, float]):
        self.count = count
        self.species_distribution = species_distribution
        self.world: WorldMap | None = None


    def generate_plants(self, world: WorldMap) -> WorldMap:
        self.world = world

        for specie, fraction   in self.species_distribution:
            amount = int(fraction * self.count)
            available_positions = self._get_valid_positions(world.height, world.width, specie)
            approved_positions = self._get_random_positons(available_positions, amount)

            for position in approved_positions:
                plant = specie(
                    name=specie.__name__,
                    position=position,
                    allowed_terrains=specie.allowed_terrains
                )
                world.add_organism(plant)


        return world







    def _get_valid_positions(self, height: int, width: int, plant: Plant) -> list[Position]:
        return [
            Position(x, y)
            for x in range (height)
            for y in range (width)
            if self._is_valid_position(Position(x,y), plant)
        ]


    def _is_valid_position(self, position: Position, plant: Plant) -> bool:
        tile = self.world.get_tile_by_position(position)
        return tile.terrain in plant.allowed_terrains


    def _get_random_positons(self, available_positions: list[Position], count) -> list[Position]:
        if not available_positions or len(available_positions) < count:
            return []

        return random.sample(available_positions, count)







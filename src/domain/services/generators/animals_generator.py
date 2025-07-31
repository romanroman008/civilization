import random

from domain.components.position import Position
from domain.organism.instances.animal import Animal
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.world_map.world_facade import WorldFacade


def _get_random_positions(positions: list[Position], amount: int) -> list[Position]:
    return random.sample(positions, k=min(amount, len(positions)))


class AnimalsGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[OrganismPrefab, float]]):
        self.count = count
        self.species_distribution = species_distribution
        self.world_facade: WorldFacade | None = None

    def generate(self, world_facade: WorldFacade) -> WorldFacade:
        self.world_facade = world_facade

        for organism_prefab, fraction in self.species_distribution:
            amount = int(fraction * self.count)
            available_positions = self._get_valid_positions(world_facade.height, world_facade.width, organism_prefab)
            approved_positions = _get_random_positions(available_positions, amount)
            animal_prefab = OrganismPrefab(organism_prefab.name, organism_prefab.allowed_terrains)

            for position in approved_positions:
                animal = Animal(animal_prefab, position)
                world_facade.add_organism(animal)

        return world_facade

    def _get_valid_positions(self, height: int, width: int, organism: OrganismPrefab) -> list[Position]:
        return [
            Position(x, y)
            for y in range(height)
            for x in range(width)
            if self.world_facade.is_position_allowed(Position(x, y), organism.allowed_terrains)
        ]

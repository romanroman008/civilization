import random


from domain.components.position import Position
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.world_map.world_map import WorldMap


def _get_random_positions(positions: list[Position], amount:int) -> list[Position]:
    return random.sample(positions, k=min(amount, len(positions)))



class HumanGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[OrganismPrefab, float]]):
        self.count = count
        self.species_distribution = species_distribution
        self.world: WorldMap | None = None


    def generate(self, world: WorldMap) -> WorldMap:
        self.world = world

        for organism, fraction   in self.species_distribution:
            amount = int(fraction * self.count)
            available_positions = self._get_valid_positions(world.height, world.width, organism)
            approved_positions = _get_random_positions(available_positions, amount)
            animal_prefab = OrganismPrefab(organism.name, organism.allowed_terrains)

            for position in approved_positions:
                human = Human(animal_prefab, position)
                world.add_organism(human)


        return world



    def _get_valid_positions(self, height: int, width: int, organism: OrganismPrefab) -> list[Position]:
        return [
            Position(x, y)
            for y in range (height)
            for x in range (width)
            if self._is_valid_position(Position(x,y), organism)
        ]


    def _is_valid_position(self, position: Position, organism: OrganismPrefab) -> bool:
        tile = self.world.get_tile_by_position(position)
        return tile.terrain in organism.allowed_terrains






import random


from domain.components.position import Position
from domain.organism.brain.brain import Brain

from domain.organism.factory.human_factory import HumanFactory



from domain.organism.instances.human import Human
from domain.organism.prefabs.organism_prefab import OrganismPrefab


from domain.world_map.world_facade import WorldFacade





def _get_random_positions(positions: list[Position], amount:int) -> list[Position]:
    return random.sample(positions, k=min(amount, len(positions)))




class HumanGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[OrganismPrefab, float]]):
        self._count = count
        self._species_distribution = species_distribution
        self._world_facade: WorldFacade | None = None
        self._human_factory: HumanFactory | None = None


    def generate(self, world_facade: WorldFacade) -> WorldFacade:
        self._world_facade = world_facade
        event_bus = world_facade.event_bus
        self._human_factory = HumanFactory(world_facade.vision_port, event_bus)


        for prefab, fraction in self._species_distribution:
            amount = int(fraction * self._count)
            available_positions = self._get_valid_positions(world_facade.height, world_facade.width, prefab)
            approved_positions = _get_random_positions(available_positions, amount)


            for position in approved_positions:
                position = Position(3,3)
                human = self._human_factory.create(prefab, position)
                world_facade.add_organism(human)


        return world_facade



    def _get_valid_positions(self, height: int, width: int, organism: OrganismPrefab) -> list[Position]:
        return [
            Position(x, y)
            for y in range (height)
            for x in range (width)
            if self._world_facade.is_position_allowed(Position(x, y), organism.allowed_terrains)
        ]









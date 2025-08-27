import random


from domain.components.position import Position
from domain.organism.factory.plant_factory import PlantFactory
from domain.organism.instances.plant import Plant
from domain.organism.prefabs.plant_prefab import PlantPrefab
from domain.world_map.world_facade import WorldFacade



class PlantsGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[PlantPrefab, float]]):
        self._count = count
        self._species_distribution = species_distribution
        self._world_facade: WorldFacade | None = None
        self._plant_factory: PlantFactory | None = None



    def generate_plants(self, world_facade: WorldFacade) -> WorldFacade:
        self._world_facade = world_facade
        self._plant_factory = PlantFactory(world_facade.event_bus)

        for plant_pref, fraction   in self._species_distribution:
            amount = int(fraction * self._count)
            available_positions = self._get_valid_positions(world_facade.height, world_facade.width, plant_pref)
            approved_positions = self._get_random_positions_with_blocking(available_positions, plant_pref, amount)


            for position in approved_positions:
                plant = self._plant_factory.create(plant_pref, position)
                world_facade.add_organism(plant)


        return world_facade




    def _get_valid_positions(self, height: int, width: int, plant_pref: PlantPrefab) -> list[Position]:
        return [
            Position(x, y)
            for y in range (height)
            for x in range (width)
            if self._world_facade.is_position_allowed(Position(x, y), plant_pref.allowed_terrains)
        ]



    def _get_random_positions_with_blocking(
            self,
            candidates: list[Position],
            plant_pref: PlantPrefab,
            count: int
    ) -> list[Position]:

        selected: list[Position] = []
        available = candidates[:]
        random.shuffle(available)
        blocked_set: set[tuple[int, int]] = set()


        for pos in available:
            if (pos.x, pos.y) in blocked_set:
                continue

            blocked_area = self._get_blocked_area(pos, plant_pref.block_radius)
            blocked_coords = {(p.x, p.y) for p in blocked_area}

            if blocked_coords & blocked_set:
                continue

            selected.append(pos)
            blocked_set.update(blocked_coords)

            if len(selected) >= count:
                break



        return selected

    def _get_blocked_area(self, position: Position, radius: int) -> list[Position]:
        cx, cy = position.x, position.y
        area = [
            Position(cx + dx, cy + dy)
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)
        ]
        return [pos for pos in area if 0 <= pos.x < self._world_facade.width and 0 <= pos.y < self._world_facade.height]







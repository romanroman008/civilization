import random

from domain.world.entieties.organism.plant import Plant
from domain.world.entieties.position import Position
from domain.world.entieties.world_map import WorldMap


class PlantsGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[Plant, float]]):
        self.count = count
        self.species_distribution = species_distribution
        self.world: WorldMap | None = None


    def generate_plants(self, world: WorldMap) -> WorldMap:
        self.world = world

        for specie, fraction   in self.species_distribution:
            amount = int(fraction * self.count)
            available_positions = self._get_valid_positions(world.height, world.width, specie)
            approved_positions = self._get_random_positions_with_blocking(available_positions, specie, amount)


            for position in approved_positions:
                plant = Plant(specie.name, specie.allowed_terrains, position)
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

    def _get_random_positions_with_blocking(
            self,
            candidates: list[Position],
            plant: Plant,
            count: int
    ) -> list[Position]:
        selected: list[Position] = []
        available = candidates[:]
        random.shuffle(available)
        blocked_set: set[tuple[int, int]] = set()

        for pos in available:
            if (pos.x, pos.y) in blocked_set:
                continue

            blocked_area = self.get_blocked_area(pos, plant.block_radius)
            blocked_coords = {(p.x, p.y) for p in blocked_area}

            if blocked_coords & blocked_set:
                continue

            selected.append(pos)
            blocked_set.update(blocked_coords)

            if len(selected) >= count:
                break

        return selected

    def get_blocked_area(self, position: Position, radius: int) -> list[Position]:
        cx, cy = position.x, position.y
        area = [
            Position(cx + dx, cy + dy)
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)
        ]
        return [pos for pos in area if 0 <= pos.x < self.world.width and 0 <= pos.y < self.world.height]







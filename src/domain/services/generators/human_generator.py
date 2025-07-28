import random
from typing import Sequence

from domain.components.position import Position
from domain.human.brain import Brain
from domain.human.field_of_view import FieldOfView
from domain.human.vitals import Vitals
from domain.organism.human_movement import HumanMovement
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.world_map.tile import Tile
from domain.world_map.world_map import WorldMap
from domain.world_map.world_perception import WorldPerception


def _get_random_positions(positions: list[Position], amount:int) -> list[Position]:
    return random.sample(positions, k=min(amount, len(positions)))

def create_vitals():
    return  Vitals()

def create_world_perception(tiles: Sequence[Tile], width: int, height: int) -> WorldPerception:
    return WorldPerception(tiles, width, height)

def create_field_of_view(radius: int, world_perception: WorldPerception) -> FieldOfView:
    return FieldOfView(radius, world_perception)

def create_movement(position: Position) -> HumanMovement:
    return HumanMovement(position)

def create_brain(movement:HumanMovement, world_perception:WorldPerception) -> Brain:
    field_of_view = create_field_of_view(5,world_perception)
    vitals = create_vitals()

    return Brain(field_of_view, vitals, movement)



class HumanGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[OrganismPrefab, float]]):
        self.count = count
        self.species_distribution = species_distribution
        self.world: WorldMap | None = None


    def generate(self, world: WorldMap) -> WorldMap:
        self.world = world
        world_perception = create_world_perception(self.world.tiles, self.world.width, self.world.height)

        for organism, fraction   in self.species_distribution:
            amount = int(fraction * self.count)
            available_positions = self._get_valid_positions(world.height, world.width, organism)
            approved_positions = _get_random_positions(available_positions, amount)
            animal_prefab = OrganismPrefab(organism.name, organism.allowed_terrains)

            for position in approved_positions:

                movement = create_movement(position)
                brain = create_brain(movement, world_perception)
                human = Human(animal_prefab, position, brain, movement)
                world.add_organism(human)


        return world



    def _get_valid_positions(self, height: int, width: int, organism: OrganismPrefab) -> list[Position]:
        return [
            Position(x, y)
            for y in range (height)
            for x in range (width)
            if self.world.is_position_allowed(Position(x,y), organism.allowed_terrains)
        ]









import random

from domain import world
from domain.world.entieties.direction import Direction
from domain.world.entieties.organism.animal import Animal
from domain.world.entieties.organism.organism import Organism
from domain.world.entieties.position import Position
from domain.world.entieties.world_map import WorldMap


class MovementSystem:
    def __init__(self, world_map: WorldMap):
        self.world = world_map
        self.animals = [o for o in world_map.organisms if isinstance(o, Animal)]


    def move_animal(self, animal: Animal):
        if not animal.is_alive:
            return
        directions = self.get_valid_directions(animal)
        chosen_direction = random.choice(directions)
        new_position = animal.position + chosen_direction.vector()




        animal.position = new_position




    def get_valid_directions(self, organism: Organism):
        valid_directions = []
        position = organism.position
        for d in Direction:
            pos = position + d.vector()

            if not self.world.is_position_available(pos):
                continue

            if not self.is_terrain_allowed(self.world.get_tile_by_position(pos), organism):
                continue

            valid_directions.append(d)

        return valid_directions

    def is_terrain_allowed(self, tile, organism: Organism):
        if tile.terrain in organism.allowed_terrains:
            return True
        return False

    def __call__(self, tick_numbers: int):
        for animal in self.animals:
            print("moving animal", animal.position)
            self.move_animal(animal)
from __future__ import annotations
import random

from domain.components.direction import Direction

from domain.components.position import Position
from domain.components.terrain import Terrain
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from domain.organism.instances.animal import Animal
    from domain.organism.instances.human import Human


from domain.world_map.world_map import WorldMap









class MovementSystem:

    def __init__(self, logger, world_map: WorldMap):
        from domain.organism.instances.animal import Animal
        from domain.organism.instances.human import Human
        self._counter = 0
        self.logger = logger
        self.world = world_map
        self.animals = [o for o in world_map.organisms if isinstance(o, Animal)]
        self.humans = [o for o in world_map.organisms if isinstance(o, Human)]
        self._set_finalize_movement_call(self.animals, self.humans)


    def _set_finalize_movement_call(self, animals:list[Animal], humans: list[Human]):
        for animal in animals:
            animal.add_finalized_move(self.update_organism_occupied_position)




    def update_organism_occupied_position(self, prev: Position, new: Position):
        prev_tile = self.world.get_tile_by_position(prev)
        animal = prev_tile.organism
        prev_tile.remove_organism()
        act_tile = self.world.get_tile_by_position(new)
        act_tile.add_organism(animal)

    def move_animal(self, animal: Animal):
        directions = self._get_valid_directions(animal)
        if not directions:
            return
        chosen_direction = random.choice(directions)
        animal.move(chosen_direction)
        self.world.set_as_move_target(animal.target_position)

    def move_human(self, human: Human):
        directions = self._get_valid_directions(human)
        if not directions:
            return
        chosen_direction = random.choice(directions)
        human.move(chosen_direction)
        self.world.set_as_move_target(human.target_position)




    def _get_valid_directions(self, organism: Organism):
        valid_directions = []
        position = organism.position
        for d in Direction:
            pos = position + d.vector()
            if self.world.is_position_allowed(pos, organism.allowed_terrains):
                valid_directions.append(d)

        return valid_directions




    def __call__(self, interval:float, *args, **kwargs):
        self._counter += 1
        for animal in self.animals:
            if animal.is_moving:
                continue
          #  self.move_animal(animal)

        for human in self.humans:
            if human.is_moving:
                continue
            # self.move_human(human)


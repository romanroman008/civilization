from __future__ import annotations
import random

from domain.components.direction import Direction

from domain.components.position import Position
from domain.components.terrain import Terrain
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from domain.organism.instances.animal import Animal
    from domain.organism.instances.human import Human

from domain.organism.instances.organism import Organism
from domain.world_map.world_map import WorldMap


def _is_terrain_allowed(tile, allowed_terrains: list[Terrain]):
    if tile.terrain in allowed_terrains:
        return True
    return False

def find_needed_offset(organism) -> tuple[float,float]:
    offset_x = organism.target_position.x - organism.position.x
    offset_y = organism.target_position.y - organism.position.y
    return offset_x, offset_y

def find_target_position(actual:Position, direction: Direction, distance: int):
    return actual + direction.vector() * distance

def find_needed_direction(actual_position: Position, target_position: Position) -> Direction:
    position_diff = target_position - actual_position

    if position_diff == Direction.LEFT.vector():
        return Direction.LEFT
    if position_diff == Direction.TOP.vector():
        return Direction.TOP
    if position_diff == Direction.RIGHT.vector():
        return Direction.RIGHT
    if position_diff == Direction.BOT.vector():
        return Direction.BOT
    return Direction.IDLE


def find_shortest_rotation(current: Direction, desired: Direction) -> float:
    current_angle = current.angle
    desired_angle = desired.angle

    rotation = desired_angle - current_angle

    if rotation > 180:
        rotation -= 360
    elif rotation < -180:
        rotation += 360


    return rotation






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

        for human in humans:
            human.add_finalized_move(self.update_organism_occupied_position)


    def update_organism_occupied_position(self, prev: Position, new: Position):
        prev_tile = self.world.get_tile_by_position(prev)
        animal = prev_tile.organisms[0]
        prev_tile.remove_organism(animal)
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
            if self._is_move_valid(pos, organism.allowed_terrains):
                valid_directions.append(d)

        return valid_directions

    def _is_move_valid(self, pos: Position, allowed_terrains: list[Terrain]) -> bool:
        if not self.world.is_position_available(pos):
            return False
        if not _is_terrain_allowed(self.world.get_tile_by_position(pos), allowed_terrains):
            return False
        return True




    def __call__(self, interval:float, *args, **kwargs):
        self._counter += 1
        for animal in self.animals:
            if animal.is_moving:
                continue
            self.move_animal(animal)

        for human in self.humans:
            if human.is_moving:
                continue
            self.move_human(human)


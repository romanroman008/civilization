import random

from domain.components.direction import Direction
from domain.entieties.organism.animal import Animal
from domain.entieties.organism.organism import Organism
from domain.components.position import Position
from domain.entieties.world_map import WorldMap


def _is_terrain_allowed(tile, organism: Organism):
    if tile.terrain in organism.allowed_terrains:
        return True
    return False

def _find_needed_rotation(organism: Organism) -> Direction:
    position_diff = organism.target_position - organism.position

    if position_diff == Direction.LEFT.vector():
        return Direction.LEFT
    if position_diff == Direction.TOP.vector():
        return Direction.TOP
    if position_diff == Direction.RIGHT.vector():
        return Direction.RIGHT
    if position_diff == Direction.BOT.vector():
        return Direction.BOT
    return Direction.IDLE

def _find_shortest_rotation(current: Direction, desired: Direction) -> float:
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
        self.logger = logger
        self.world = world_map
        self.animals = [o for o in world_map.organisms if isinstance(o, Animal)]


    def move_animal(self, animal: Animal):
        if not animal.is_alive:
            return
        animal.isMoving = True
        directions = self._get_valid_directions(animal)
        chosen_direction = random.choice(directions)

        #with animal.lock:
        new_position = animal.position + chosen_direction.vector()
        animal.target_position = new_position
        target_direction =  _find_needed_rotation(animal)
        animal.target_rotation = _find_shortest_rotation(animal.facing, target_direction)
        if target_direction == Direction.IDLE:
            animal.isMoving = False
            animal.target_rotation = animal.rotation
            return

        animal.target_facing = target_direction





    def _get_valid_directions(self, organism: Organism):
        valid_directions = []
        position = organism.position
        for d in Direction:
            pos = position + d.vector()
            if self._is_move_valid(pos, organism):
                valid_directions.append(d)

        return valid_directions

    def _is_move_valid(self, pos: Position, organism: Organism) -> bool:
        if not self.world.is_position_available(pos):
            return False
        if not _is_terrain_allowed(self.world.get_tile_by_position(pos), organism):
            return False
        return True




    def __call__(self, interval:float, *args, **kwargs):
        for animal in self.animals:
            if animal.isMoving:
                continue
            self.move_animal(animal)

            self.logger.debug(f"Animal: {animal.name} moved to {animal.position}")
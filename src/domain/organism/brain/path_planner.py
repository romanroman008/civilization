from collections import deque
from typing import Optional, Deque

from domain.components.direction import Direction
from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.perception.vision import Vision
from domain.organism.transform.transform import TransformReadOnly


class PathPlanner:
    def __init__(self, vision:Vision, transform: TransformReadOnly, available_terrains:set[Terrain]):
        self._available_terrains = available_terrains
        self._transform = transform
        self._vision = vision

    def find_shortest_path(self, goal: tuple[int, int], start: tuple[int,int] = None) -> Optional[list[Direction]]:
        queue = deque()
        if not start:
            start = self._transform.position.x, self._transform.position.y
        queue.append((start, []))
        visited = set()
        visited.add(start)

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            for direction, neighbour_pos in self._get_possible_move_neighbours(current).items():
                if neighbour_pos in visited:
                    continue
                visited.add(neighbour_pos)
                queue.append((neighbour_pos, path + [direction]))

        return None


    def _get_possible_move_neighbours(self, current_position: tuple[int,int]) -> dict[Direction, tuple[int,int]]:
        neighbours = self._vision.get_neighbours_with_allowed_terrains(Position(current_position[0], current_position[1]))
        to_direction = Direction.to_direction
        result = {}

        for neighbour_position in neighbours:
            relative_positon =  (neighbour_position[0] - current_position[0], neighbour_position[1] - current_position[1])
            direction = to_direction(relative_positon)
            result[direction] = neighbour_position



        return result





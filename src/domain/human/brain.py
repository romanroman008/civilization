from collections import deque
from typing import Optional

from domain.components.direction import Direction
from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.human.field_of_view import FieldOfView
from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.human.vitals import Vitals



class Brain:
    def __init__(self, field_of_view: FieldOfView, vitals: Vitals):
        self._field_of_view = field_of_view
        self._vitals = vitals
        self._organism_data: list[OrganismInfo] = []
        self._perceived_objects: list[PerceivedObject] = []


    def update(self, perceived_objects: list[PerceivedObject]):
        self._perceived_objects = perceived_objects



    def find_shortest_path(self, start: Position, goal: Position) -> Optional[list[Direction]]:
        queue = deque()
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



    def _get_possible_move_neighbours(self, position: Position) -> dict[Direction,Position]:
        neighbours: dict[Direction,Position] = {}
        for direction in Direction:
            neighbour_pos = position + direction.vector()
            for perc_obj in self._perceived_objects:
                if perc_obj.relative_position == neighbour_pos and perc_obj.terrain == Terrain.GRASS:
                    neighbours[direction] = neighbour_pos
                    break

        return neighbours













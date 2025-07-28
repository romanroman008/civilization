import asyncio
from collections import deque
from typing import Optional

from domain.components.direction import Direction
from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.human.field_of_view import FieldOfView

from domain.human.perception.animal_info import AnimalInfo
from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.human.vitals import Vitals
from domain.organism.human_movement import HumanMovement


class Brain:
    def __init__(self, field_of_view: FieldOfView, vitals: Vitals, movement: HumanMovement):
        self._field_of_view = field_of_view
        self._vitals = vitals
        self._movement = movement

        self._organism_data: list[OrganismInfo] = []
        self._perceived_objects: list[PerceivedObject] = []
        self._target: Optional[OrganismInfo] = None

        self.is_hunting = False


    def tick(self, position: Position):
        self._field_of_view.update(position)
        self._perceived_objects = self._field_of_view.get_perceived_objects()
        self._check_target_visibility()

    def update(self):
        pass


    async def hunt(self):
        self.is_hunting = True
        closest_animal = self._field_of_view.detect_closest_animal()

        if closest_animal is None:
            return
        self._target = closest_animal
        if closest_animal.is_visible:
            path = self.find_shortest_path(closest_animal.relative_position)
            await self._execute_move_sequence(path)
            self.is_hunting = False


    def _check_target_visibility(self):
        if self._target is None:
            return

        match = next(
            (
                (perc_obj for perc_obj in self._perceived_objects
                 if perc_obj.organism_info and perc_obj.organism_info.id == self._target.id)
            ),
            None
        )
        if match:
            self._target.got_sighting(match.organism_info.relative_position)
        else:
            self._target.lost_sighting()



    async def _execute_move_sequence(self, directions: list[Direction]):
        for direction in directions:
            self._movement.start_move(direction, 1)
            await self._movement.wait_until_stop()




    def find_shortest_path(self, goal: Position, start: Position = Position(0, 0)) -> Optional[list[Direction]]:
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

    def _get_possible_move_neighbours(self, position: Position) -> dict[Direction, Position]:
        neighbours: dict[Direction, Position] = {}
        perceived_map = {
            obj.relative_position: obj
            for obj in self._perceived_objects
        }

        for direction in Direction:
            neighbour_pos = position + direction.vector()
            obj = perceived_map.get(neighbour_pos)
            if obj and obj.terrain == Terrain.GRASS:
                neighbours[direction] = neighbour_pos

        return neighbours

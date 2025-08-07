
import logging
from collections import deque
from typing import Optional

from domain.components.direction import Direction
from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.human.field_of_view import FieldOfView

from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.human.vitals import Vitals
from domain.organism.human_movement import HumanMovement
from domain.organism.instances.human import Human


from domain.organism.state.hunting_state import HuntingState
from domain.organism.state.idle_state import IdleState
from domain.organism.state.walking_state import WalkingState
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult
from shared.logger import get_logger


def _get_possible_move_neighbours(position: Position, perceived_objects: list[PerceivedObject]) -> dict[
    Direction, Position]:
    neighbours: dict[Direction, Position] = {}
    perceived_map = {
        obj.relative_position: obj
        for obj in perceived_objects
    }

    for direction in Direction:
        neighbour_pos = position + direction.vector()
        obj = perceived_map.get(neighbour_pos)
        if obj and obj.terrain == Terrain.GRASS:
            neighbours[direction] = neighbour_pos

    return neighbours


def find_shortest_path(goal: Position, perceived_objects: list[PerceivedObject]) -> Optional[list[Direction]]:
    queue = deque()
    start = Position(0, 0)
    queue.append((start, []))
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        for direction, neighbour_pos in _get_possible_move_neighbours(current, perceived_objects).items():
            if neighbour_pos in visited:
                continue
            visited.add(neighbour_pos)
            queue.append((neighbour_pos, path + [direction]))

    return None


class HumanBrain:
    def __init__(self, field_of_view: FieldOfView, vitals: Vitals, movement: HumanMovement, event_bus: EventBus):
        self._field_of_view = field_of_view
        self._vitals = vitals
        self._human: Optional[Human] = None
        self._movement = movement

        self._organism_data: list[OrganismInfo] = []
        self._perceived_objects: list[PerceivedObject] = []
        self._target: Optional[OrganismInfo] = None

        self._event_bus = event_bus

        self._is_busy = False
        self._register_handlers()


    def _register_handlers(self):
        self._event_bus.on_async("position update", self.tick)

    def _initialize_logger(self):
        self._logger = get_logger(f"Human {self._human.id}", level=logging.INFO, log_filename="human.log")

    def set_human(self, human: Human):
        self._human = human
        self._field_of_view.update(self._human.position)
        self._perceived_objects = self._field_of_view.perceived_objects()
        self._check_target_visibility()
        self._initialize_logger()

    async def tick(self, payload):
        self._field_of_view.update(self._human.position)
        self._perceived_objects = self._field_of_view.perceived_objects()
        self._check_target_visibility()

    async def decide(self):
        if self._human.state != IdleState:
            return

        path = await self.hunt()

        if path is None:
            await self._human.set_state(IdleState())
        await self._human.set_state(HuntingState(path))

    async def walk(self, direction: Direction):
        result = await self.emit_walking_decision(direction)
        if result is MoveResult.SUCCESS:
            await self._human.set_state(WalkingState())
            await self._movement.move_to(direction)
            await self._notify_position_change()
            await self._human.set_state(IdleState())



    async def hunt(self):
        closest_animal = self._field_of_view.detect_closest_animal()
        if closest_animal is None:
            return []
        self._target = closest_animal
        self._logger.info(f"has started hunting for: {self._target.id}, "
                          f"position {self._target.relative_position},"
                          f"last seen {self._target.last_seen_position}")
        path = []
        if closest_animal.is_visible:
            path = find_shortest_path(closest_animal.relative_position, self._perceived_objects)
        else:
            path = find_shortest_path(closest_animal.last_seen_position, self._perceived_objects)
        self._logger.info(f"walking sequence: {path}")
        await self._human.set_state(HuntingState())
        for direction in path:
            await self.walk(direction)
        await self._human.set_state(IdleState())


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


    async def _notify_position_change(self):
        payload = {
            "organism_id": self._human.id,
            "position": self._human.position
        }

        await self._event_bus.emit("position_change", payload)



    async def emit_walking_decision(self, move_direction: Direction):
        target_position = self._direction_to_position(move_direction)
        try:
            result = await self._event_bus.emit_with_response("change_state_requested",{
                "organism": self._human,
                "new_state": "WalkingState",
                "target_position": target_position
            })
            if result == MoveResult.SUCCESS:
                self._logger.info(f"has started walking from {self._human.position} to {target_position}")
            elif result == MoveResult.OUT_OF_BOUNDS:
                self._logger.info(f"Position {target_position} is out of bounds")
            elif result == MoveResult.RESERVED:
                self._logger.info(f"Position {target_position} is reserved")
            else:
                self._logger.info(f"Position {target_position} is occupied")
            return result

        except Exception as e:
            self._logger.exception(f"Failed to request state change: {e}")


    def _direction_to_position(self, direction: Direction) -> Position:
        return direction.vector() + self._human.position

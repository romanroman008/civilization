import logging
from collections import deque
from typing import Deque

from domain.components.direction import Direction
from domain.components.position import Position
from domain.organism.brain.brain_interactions_handler import BrainInteractionsHandler
from domain.organism.brain.path_planner import PathPlanner
from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.movement import Movement
from domain.organism.perception.target_info import TargetInfo
from domain.organism.perception.vision import Vision
from domain.organism.transform.transform import TransformReadOnly
from shared.logger import get_logger


class Hunting:
    def __init__(self,
                 movement: Movement,
                 path_planner: PathPlanner,
                 vision: Vision,
                 transform: TransformReadOnly
                 ):
        self._movement = movement
        self._path_planner = path_planner
        self._vision = vision
        self._transform = transform
        self._brain_interactions_handler: BrainInteractionsHandler | None = None

        self._target: TargetInfo | None = None
        self._path: Deque[Direction] | None = None
        self._distance_to_target: int = -1
        self._last_target_position: Position | None = None

        self._range = 1


        self._status: ActionStatus = ActionStatus.IDLE

        self._logger = get_logger("Hunting", level=logging.INFO, log_filename="hunting.log")


    def set_brain_interactions_handler(self, brain_interactions: BrainInteractionsHandler):
        self._brain_interactions_handler = brain_interactions


    def hunt(self, target: TargetInfo | None = None):
        if target is None:
            self._target = self._vision.detect_closest_alive_animal()

        if self._target is None:
            self._logger.error("No target not within sight")
            return

        self._path = deque(self._plan_path_to_target())
        self._last_target_position = self._target.position
        if len(self._path) <= 1:
            self._kill()

        self._status = ActionStatus.RUNNING



    def tick(self) -> ActionStatus:
        if self._status == ActionStatus.IDLE:
            return ActionStatus.IDLE

        movement_status = self._movement.tick()
        if (movement_status == ActionStatus.IDLE) or (movement_status == ActionStatus.SUCCESS):
            self._target = self._vision.update(self._target)
            self._path = self._plan_path_to_target()

            distance_to_target = self._get_distance_to_target()

            if distance_to_target <= self._range:
                self._finish()
                self._status = ActionStatus.IDLE
                return self._status
            else:
                direction = self._path.pop()
                self._movement.move(direction)
        return self._status



    def _finish(self):
        kill_request_result = self._kill()
        if kill_request_result:
            self._logger.info(f"Target {self._target.id} successfully killed")
            self._status = ActionStatus.IDLE
        else:
            self._logger.info(f"Kill request {self._target.id} denied")
            self._status = ActionStatus.IDLE


    def _kill(self) -> bool:
        return self._brain_interactions_handler.emit_kill_decision(self._target.id)

    def _get_distance_to_target(self):
        x, y = self._transform.position.x, self._transform.position.y
        target_x, target_y = self._target.position
        offset_x, offset_y = self._target.offset
        target_x += offset_x / 100
        target_y += offset_y / 100
        return abs(target_x - x) + abs(target_y - y)

    def _plan_path_to_target(self):
        destination = (
            self._target.position if self._target.is_visible
            else self._target.last_seen_position
        )
        return self._path_planner.find_shortest_path(destination)




    def recompose_path(self):
        target = self._vision.update(target=self._target)

        prev_position = self._last_target_position


        if target.is_visible:
            actual_position = target.position
        else:
            actual_position = target.last_seen_position

        position_diff = actual_position - prev_position
        self._last_target_position = actual_position


        if prev_position < actual_position:
            self._path.append(Direction.to_direction(position_diff))

        if prev_position > target.last_seen_position:
            self._path.append(Direction.reverse_direction(position_diff))





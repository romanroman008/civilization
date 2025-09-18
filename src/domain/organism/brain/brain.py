import logging
from collections import deque
from typing import Optional

from domain.components.direction import Direction
from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.brain.brain_interactions_handler import BrainInteractionsHandler
from domain.organism.brain.path_planner import PathPlanner
from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.organism_id import OrganismID


from domain.organism.perception.target_info import TargetInfo
from domain.organism.perception.vision import Vision
from domain.organism.strategy.idle_strategy import IdleStrategy
from domain.organism.transform.transform import TransformReadOnly

from domain.organism.vitals import Vitals

from domain.organism.movement.movement import Movement

from domain.organism.state.hunting_state import HuntingState
from domain.organism.state.idle_state import IdleState
from domain.organism.state.walking_state import WalkingState

from domain.organism.strategy.random_walk_strategy import RandomWalkStrategy
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult
from shared.logger import get_logger



class Brain:
    DECIDE_BUCKETS = 20

    def __init__(self,
                 vision: Vision,
                 vitals: Vitals,
                 movement: Movement,
                 path_planner: PathPlanner,
                 transform_readonly: TransformReadOnly,
                 available_terrains: set[Terrain],
                 event_bus: EventBus):



        self._owner_id: OrganismID | None = None

        self._vision = vision
        self._vitals = vitals
        self._movement = movement
        self._path_planner = path_planner
        self._transform_readonly = transform_readonly
        self._available_terrains = available_terrains

        self._decision_strategy = RandomWalkStrategy()


        self._target: Optional[TargetInfo] = None

        self._event_bus: EventBus = event_bus
        self._brain_interactions_handler: BrainInteractionsHandler | None = None

        self._status: ActionStatus = ActionStatus.IDLE
        self._is_alive = True

        self._range = 1

        self._phase = 0


    @property
    def is_alive(self) -> bool:
        return self._is_alive


    def _initialize_logger(self):
        self._logger = get_logger(f"Organism {self._owner_id}", level=logging.INFO, log_filename="organism.log")

    def _create_brain_interactions_handler(self):
        return BrainInteractionsHandler(owner_id=self._owner_id,
                                        brain=self,
                                        transform_readonly=self._transform_readonly,
                                        vision=self._vision,
                                        event_bus=self._event_bus)

    def _can_decide_this_tick(self, tick:int):
        return (tick % self.DECIDE_BUCKETS) == self._phase

    def tick(self, tick:int):
        if not self._is_alive:
            return


        status = self._movement.tick()
        if status == ActionStatus.SUCCESS:
            self._brain_interactions_handler.notify_position_change()
            status = ActionStatus.IDLE

        self._status = status

        if self._status is ActionStatus.IDLE and self._can_decide_this_tick(tick):
            self._vision.update()
            self._decision_strategy.decide(self)




    def set_owner_id(self, organism_id: OrganismID):
        if self._owner_id:
            raise RuntimeError(f"Brain {organism_id} already has an owner")
        self._owner_id = organism_id
        self._brain_interactions_handler = self._create_brain_interactions_handler()
        self._phase = organism_id.id % self.DECIDE_BUCKETS
        self._initialize_logger()


    def walk(self, direction: Direction):
        if (not self._is_alive) or (self._status is not ActionStatus.IDLE):
            return

        result = self._brain_interactions_handler.emit_walking_decision(direction)
        if result == MoveResult.SUCCESS:
          #  self._logger.info(f"Brain {self._owner_id} has started walking to {direction}")
            self._movement.move(direction)
        else:
            self._logger.error(f"Brain {self._owner_id} has failed to walk {direction} due to {result}")


    def get_possible_moves(self):
        return [d - self._transform_readonly.position
            for d in self._vision.get_possible_move_positions()
            ]



    def _is_target_in_range(self):
        if self._target.position.distance_to(Position(0, 0)) <= self._range:
            return True
        return False




    def kill_itself(self):
        self._is_alive = False



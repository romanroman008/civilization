import logging

from domain.components.terrain import Terrain
from domain.organism.brain.brain import Brain
from domain.organism.brain.path_planner import PathPlanner
from domain.organism.movement.human_movement import HumanMovement
from domain.organism.perception.vision import Vision
from domain.organism.transform.transform import TransformReadOnly

from domain.organism.vitals import Vitals

from domain.organism.strategy.idle_strategy import IdleStrategy

from domain.services.event_bus import EventBus
from shared.logger import get_logger


class HumanBrain(Brain):
    def __init__(self,
                 vision: Vision,
                 vitals: Vitals,
                 movement: HumanMovement,
                 path_planner: PathPlanner,
                 transform_readonly: TransformReadOnly,
                 allowed_terrains: set[Terrain],
                 event_bus: EventBus):
        super().__init__(vision, vitals, movement, path_planner, transform_readonly, allowed_terrains, event_bus)


        self._decision_strategy = IdleStrategy()

    def _initialize_logger(self):
        self._logger = get_logger(f"Human {self._owner_id}", level=logging.INFO, log_filename="human.log")



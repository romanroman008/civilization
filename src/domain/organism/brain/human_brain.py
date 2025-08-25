import logging

from typing import Optional

from domain.organism.brain.brain import Brain
from domain.organism.perception.field_of_view import FieldOfView

from domain.organism.perception.organism_info import OrganismInfo
from domain.organism.perception.percived_object import PerceivedObject
from domain.organism.vitals import Vitals
from domain.organism.human_movement import HumanMovement
from domain.organism.instances.human import Human
from domain.organism.strategy.idle_strategy import IdleStrategy

from domain.services.event_bus import EventBus
from shared.logger import get_logger


class HumanBrain(Brain):
    def __init__(self, field_of_view: FieldOfView, vitals: Vitals, movement: HumanMovement, event_bus: EventBus):
        super().__init__(field_of_view, vitals, movement, event_bus)

        self._organism_data: list[OrganismInfo] = []
        self._perceived_objects: list[PerceivedObject] = []
        self._target: Optional[OrganismInfo] = None

        self._decision_strategy = IdleStrategy()

    def _initialize_logger(self):
        self._logger = get_logger(f"Human {self._animal.id}", level=logging.INFO, log_filename="human.log")

    def set_human(self, human: Human):
        self._animal = human
        self._field_of_view.update(self._animal.position)
        self._perceived_objects = self._field_of_view.perceived_objects()
        self._initialize_logger()

from abc import ABC

from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.pose import Pose
from domain.organism.transform.transform_readonly import TransformReadOnly

from domain.organism.transform.transform_writer import TransformWriter


class MotionAction(ABC):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly, step: float = 1):
        if step < 0:
            raise ValueError("Step must be > 0")
        self._transform_writer: TransformWriter = transform_writer
        self._transform_readonly: TransformReadOnly = transform_readonly
        self._running = False
        self._current_iteration: int = 0
        self._iterations: int = 0
        self._step: float = step
        self._rest: float = 0

    def set_target(self, target: Pose): pass

    def start(self): pass

    def step(self) -> ActionStatus: pass

    @property
    def running(self):
        return self._running


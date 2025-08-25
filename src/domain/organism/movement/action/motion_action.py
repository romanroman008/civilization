from abc import ABC

from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.transform import Transform
from domain.organism.transform_readonly import TransformReadOnly


class MotionAction(ABC):
    def __init__(self, transform: Transform, step: float = 1):
        if step < 0:
            raise ValueError("Step must be > 0")
        self._transform: Transform = transform
        self._running = False
        self._current_iteration: int = 0
        self._iterations: int = 0
        self._step: float = step
        self._rest: float = 0

    def set_target(self, target: TransformReadOnly): pass

    def start(self): pass

    def step(self) -> ActionStatus: pass

    @property
    def running(self):
        return self._running


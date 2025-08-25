import math

from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.transform import Transform
from domain.organism.transform_readonly import TransformReadOnly


class RotationAction(MotionAction):
    def __init__(self, transform: Transform, step: float = 1):
        super().__init__(transform, step)
        self._target_rotation = transform.rotation


    def set_target(self, target: TransformReadOnly):
        self._target_rotation = target.rotation

    def start(self):
        self._running = True


    def step(self) -> ActionStatus:
        if not self._running:
            return ActionStatus.IDLE

        if self._current_iteration < self._iterations - 1:
            self._transform.rotate(self._step)

        if self._current_iteration == self._iterations - 1:
            self._finish()
            return ActionStatus.SUCCESS

        self._current_iteration += 1
        return ActionStatus.RUNNING

    def _set_step_sign(self):
        self._step *= math.copysign(1,self._target_rotation)

    def _set_iterations(self):
        self._iterations = self._target_rotation // self._step

    def _set_rest(self):
        self._rest = self._target_rotation % self._step

    def _finish(self):
        self._transform.rotate(self._rest)
        self.target_rotation = self._transform.rotation
        self.current_iteration = 0
        self._running = False

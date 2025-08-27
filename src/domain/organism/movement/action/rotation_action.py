import math

from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.pose import Pose

from domain.organism.transform.transform_readonly import TransformReadOnly
from domain.organism.transform.transform_writer import TransformWriter


class RotationAction(MotionAction):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly, step: float = 1):
        super().__init__(transform_writer, transform_readonly, step)
        self._target_rotation = transform_readonly.rotation



    def set_target(self, target: Pose):
        self._target_rotation = target.rotation

    def start(self):
        self._running = True


    def step(self) -> ActionStatus:
        if not self._running:
            return ActionStatus.IDLE

        if self._current_iteration < self._iterations - 1:
            self._transform_writer.rotate(self._step)

        if self._current_iteration == self._iterations - 1:
            self._finish()
            return ActionStatus.SUCCESS

        self._current_iteration += 1
        return ActionStatus.RUNNING

    def _set_step_sign(self):
        self._step *= math.copysign(1, self._target_rotation)

    def _set_iterations(self):
        self._iterations = self._target_rotation // self._step

    def _set_rest(self):
        self._rest = self._target_rotation % self._step

    def _finish(self):
        self._transform_writer.rotate(self._rest)
        self.target_rotation = self._transform_writer.rotation
        self.current_iteration = 0
        self._running = False

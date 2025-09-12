import math

from codetiming import Timer

from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.pose import Pose
from domain.organism.transform.transform import TransformWriter, TransformReadOnly


class RotationAction(MotionAction):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly, step: int = 1):
        super().__init__(transform_writer, transform_readonly, step)
        self._target_rotation = transform_readonly.rotation
        self._target_direction = transform_readonly.direction


    def set_target(self, target: Pose):
        self._target_rotation = target.rotation
        self._target_direction = target.direction

    def start(self):
        self._running = True
        self._set_step_sign()


    def step(self) -> ActionStatus:
        if not self._running:
            return ActionStatus.IDLE


        if self._transform_readonly.direction == self._target_direction:
            self._transform_writer.match_rotation_to_direction()
            self._running = False
            return ActionStatus.SUCCESS

        self._transform_writer.rotate(self._step)
        return ActionStatus.RUNNING


    def _set_step_sign(self):
        self._step = int(math.copysign(abs(self._step), self._target_rotation))


    def _finish(self):
        self._transform_writer.rotate(self._rest)
        self.target_rotation = self._transform_readonly.rotation
        self.current_iteration = 0
        self._running = False

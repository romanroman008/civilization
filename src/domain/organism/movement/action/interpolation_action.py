import math

from domain.components.position import Position
from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.pose import Pose

from domain.organism.transform.transform_readonly import TransformReadOnly
from domain.organism.transform.transform_writer import TransformWriter


class InterpolationAction(MotionAction):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly, step: float = 1):
        super().__init__(transform_writer,transform_readonly, step)
        self._target_x = transform_readonly.x
        self._target_y = transform_readonly.y

        self._x_iterations = self._iterations
        self._y_iterations = self._iterations

        self._step_x = step
        self._step_y = step

        self._x_rest = 0
        self._y_rest = 0

        self._x_done = False
        self._y_done = False

    def set_target(self, target: Pose):
        self._target_x = target.x
        self._target_y = target.y

    def start(self):
        self._running = True

    def step(self) -> ActionStatus:
        if not self._running:
            return ActionStatus.IDLE

        if self._current_iteration < self._x_iterations - 1:
            self._transform_writer.interpolate_x(self._step_x)

        if self._current_iteration < self._y_iterations - 1:
            self._transform_writer.interpolate_y(self._step_y)

        if self.current_iteration == self._x_iterations - 1:
            self._transform_writer.interpolate_x(self._x_rest)
            self._x_done = True

        if self.current_iteration == self._y_iterations - 1:
            self._transform_writer.interpolate_y(self._y_rest)
            self._y_done = True

        if self._x_done and self._y_done:
            self._finish()
            return ActionStatus.SUCCESS

        self._current_iteration += 1
        return ActionStatus.RUNNING

    def _set_step_x_sign(self):
        self._step_x = self._step * math.copysign(1, self._target_x)

    def _set_step_y_sign(self):
        self._step_y = self._step * math.copysign(1, self._target_y)

    def _set_iterations(self):
        self._iterations = max(self._target_x // self._step_x, self._target_y // self._step_y)

    def _set_rest(self):
        self._rest = max(self._target_x % self._step_x, self._target_y % self._step_y)

    def _finish(self):
        achieved_position = Position(round(self._transform_readonly.x),
                                     round(self._transform_readonly.y))
        self._transform_writer.finalize_move(achieved_position)
        self._target_x = self._transform_readonly.x
        self._target_y = self._transform_readonly.y
        self.current_iteration = 0
        self._running = False
        self._x_done = False
        self._y_done = False

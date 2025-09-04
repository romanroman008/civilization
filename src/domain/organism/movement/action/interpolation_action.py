import math


from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.pose import Pose
from domain.organism.transform.transform import TransformWriter, TransformReadOnly


class InterpolationAction(MotionAction):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly, step: int = 1):
        super().__init__(transform_writer,transform_readonly, step)

        self._target_x = transform_readonly.x
        self._target_y = transform_readonly.y
        self._target_direction = transform_readonly.direction

        self._step_x = self._step
        self._step_y = self._step

    def set_target(self, target: Pose):
        self._target_x, self._target_y = self._transform_readonly.position + target.direction.vector()
        self._target_direction = target.direction

    def start(self):
        self._running = True
        self.set_step_x_sign()
        self.set_step_y_sign()

    def step(self) -> ActionStatus:
        if not self._running:
            return ActionStatus.IDLE

        reader = self._transform_readonly
        writer = self._transform_writer


        target_x = self._target_x
        target_y = self._target_y

        if reader.x != target_x:
            writer.interpolate_x(self._step_x)
        if reader.x == target_x:
            writer.reset_offset_x()

        if reader.y != target_y:
            writer.interpolate_y(self._step_y)
        if reader.y == target_y:
            writer.reset_offset_y()

        if reader.x == target_x and reader.y == target_y:
            self._running = False
            return ActionStatus.SUCCESS

        return ActionStatus.RUNNING


    def set_step_x_sign(self):
        self._step_x = self._step * int(math.copysign(1,self._target_direction.vector().x))

    def set_step_y_sign(self):
        self._step_y = self._step * int(math.copysign(1,self._target_direction.vector().y))







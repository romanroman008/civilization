from domain.components.direction import Direction
from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.interpolation_action import InterpolationAction
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.action.sequence_action import SequenceAction
from domain.organism.movement.movement import Movement
from domain.organism.movement.pose import Pose
from domain.organism.transform.transform import TransformWriter, TransformReadOnly


class HumanMovement(Movement):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly):
        super().__init__(transform_writer, transform_readonly)
        self._interpolation_action = InterpolationAction(transform_writer, transform_readonly)
        self._sequence_action = SequenceAction()
        self._move_status = ActionStatus.IDLE

    def move(self, target_direction: Direction):
        self._sequence_action.start(self._prepare_actions_list(target_direction))

    def tick(self):
        self._move_status = self._sequence_action.step()
        return self._move_status

    def _prepare_actions_list(self, target_direction: Direction) -> list[MotionAction]:
        target_rotation = self._transform_readonly.rotation

        target = Pose(target_direction, target_rotation)


        self._interpolation_action.set_target(target)

        return [ self._interpolation_action]

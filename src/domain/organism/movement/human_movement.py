from shapely.coordinates import transform

from domain.components.direction import Direction
from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.interpolation_action import InterpolationAction
from domain.organism.movement.action.motion_action import MotionAction
from domain.organism.movement.action.sequence_action import SequenceAction
from domain.organism.movement.movement import Movement
from domain.organism.movement.transform import Transform
from domain.organism.transform_readonly import TransformReadOnly


class HumanMovement(Movement):
    def __init__(self, transform: Transform):
        super().__init__(transform)
        self._interpolation_action = InterpolationAction(transform)
        self._sequence_action = SequenceAction()
        self._move_status = ActionStatus.IDLE

    def move(self, target_direction: Direction):
        self._sequence_action.start(self._prepare_actions_list(target_direction))

    def tick(self):
        self._move_status = self._sequence_action.step()

    def _prepare_actions_list(self, target_direction: Direction) -> list[MotionAction]:
        target_rotation = self._transform.rotation
        target_x, target_y = self._transform.translated_xy(target_direction)
        target = TransformReadOnly(target_x, target_y, target_rotation)


        self._interpolation_action.set_target(target)

        return [ self._interpolation_action]

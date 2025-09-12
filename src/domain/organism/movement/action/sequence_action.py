import logging

from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.action.motion_action import MotionAction
from shared.logger import get_logger


class SequenceAction:
    def __init__(self):
        self._actions: list[MotionAction] = []
        self._current_action: MotionAction | None = None
        self._running = False
        self._i = 0


    def start(self, actions:list[MotionAction]):
        if not actions:
            raise ValueError("Actions list is empty")
        self._running = True
        self._i = 0
        self._actions = actions
        self._current_action = self._actions[self._i]
        self._current_action.start()

    def step(self) -> ActionStatus:
        if not self._running:
            return ActionStatus.IDLE

        status = self._current_action.step()
        if status == ActionStatus.SUCCESS:
            if  self._is_last_action():
                self._finish()
                return ActionStatus.SUCCESS
            self._start_new_action()

        return ActionStatus.RUNNING


    def _is_last_action(self):
        return self._i + 1 >= len(self._actions)

    def _start_new_action(self):
        self._i += 1
        self._current_action = self._actions[self._i]
        self._current_action.start()

    def _finish(self):
        self._running = False
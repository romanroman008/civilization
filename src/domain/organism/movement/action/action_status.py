from enum import Enum, auto


class ActionStatus(Enum):
    IDLE = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILURE = auto()
from typing import Protocol

from domain.organism.perception.perception import Perception


class VisionPortProtocol(Protocol):
    def get_vision(self, observer_position, range: int) -> Perception: pass
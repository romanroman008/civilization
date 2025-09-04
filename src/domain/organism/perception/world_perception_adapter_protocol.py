from typing import Protocol

from domain.components.position import Position
from domain.organism.perception.perception import Perception


class WorldPerceptionAdapterProtocol(Protocol):
    def perception_snapshot(self, positions: list[Position]) -> Perception: pass
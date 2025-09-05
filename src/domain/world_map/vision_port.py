from __future__ import annotations
from domain.components.position import Position

from domain.organism.perception.perception import Perception

from domain.organism.perception.world_perception_adapter_protocol import WorldPerceptionAdapterProtocol
from domain.world_map.vision_port_protocol import VisionPortProtocol




class VisionPort(VisionPortProtocol):
    __slots__ = "_world_perception_adapter", "_id_registry", "_world_width", "_world_height"
    def __init__(self, world_perception_adapter: WorldPerceptionAdapterProtocol, world_width: int, world_height: int):
        self._world_perception_adapter: WorldPerceptionAdapterProtocol = world_perception_adapter
        self._world_width = world_width
        self._world_height = world_height


    def get_vision(self, observer_position: Position, range_val:int) -> Perception:
        x, y = observer_position

        x_min = max(0, x - range_val)
        y_min = max(0, y - range_val)
        x_max = min(self._world_width, x + range_val + 1)
        y_max = min(self._world_height, y + range_val + 1)

        positions = []
        append = positions.append

        for dx in range(x_min, x_max):
            for dy in range(y_min, y_max):
                append(Position(dx, dy))

        return self._world_perception_adapter.perception_snapshot(positions)










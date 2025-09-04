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

        x_min_in_bounds = max(0, min(x - range_val, self._world_width - 1))
        x_max_in_bounds = max(0, min(x + range_val + 1, self._world_width - 1))
        y_min_in_bounds = max(0, min(y - range_val, self._world_width - 1))
        y_max_in_bounds = max(0, min(y + range_val + 1, self._world_width - 1))

        positions = []
        append = positions.append

        for dx in range(x_min_in_bounds, x_max_in_bounds):
            for dy in range(y_min_in_bounds, y_max_in_bounds):
                append(Position(dx, dy))

        return self._world_perception_adapter.perception_snapshot(positions)










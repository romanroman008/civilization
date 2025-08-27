from __future__ import annotations
from domain.components.position import Position
from domain.organism.perception.percived_object import PerceivedObject
from domain.world_map.world_facade import WorldFacade


class VisionPort:
    __slots__ = "_world_facade"
    def __init__(self, world_facade: "WorldFacade"):
        self._world_facade = world_facade


    def get_vision(self, observer_position, positions: list["Position"]) -> list["PerceivedObject"]:
        return self._world_facade.get_visible_area(observer_position, positions)



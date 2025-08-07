from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.world_map.world_facade import WorldFacade


class PositionValidator:
    def __init__(self, world_facade: WorldFacade):
        self._world_facade = world_facade

    def is_position_available(self, position: Position, allowed_terrains: set[Terrain]):
        return self._world_facade.is_position_allowed(position, allowed_terrains)
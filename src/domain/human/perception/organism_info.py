from dataclasses import dataclass
from typing import Protocol, Optional

from domain.components.position import Position


class OrganismInfo(Protocol):
    def __init__(self, id, relative_position: Position, is_visible = True):
        self._id = id
        self._relative_position: Optional[Position] = relative_position
        self._is_visible = is_visible

    @property
    def id(self):
        return self._id

    @property
    def relative_position(self) -> Optional[Position]:
        return self._relative_position

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    def got_sighting(self, position: Position):
        pass

    def lost_sighting(self) -> bool:
        pass


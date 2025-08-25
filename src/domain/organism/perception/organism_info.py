
from typing import Protocol, Optional

from domain.components.position import Position
from domain.organism.organism_id import OrganismID


class OrganismInfo(Protocol):
    def __init__(self, id: OrganismID, relative_position: Position, is_alive, is_visible = True):
        self._id = id
        self._relative_position: Optional[Position] = relative_position
        self._is_visible = is_visible
        self._is_alive = is_alive

    @property
    def id(self) -> OrganismID:
        return self._id

    @property
    def relative_position(self) -> Optional[Position]:
        return self._relative_position

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    def got_sighting(self, position: Position):
        pass

    def lost_sighting(self) -> bool:
        pass

    def notify_its_death(self):
        self._is_alive = False


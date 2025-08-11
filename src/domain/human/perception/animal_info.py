from dataclasses import dataclass


from domain.components.position import Position
from domain.human.perception.organism_info import OrganismInfo

@dataclass
class AnimalInfo(OrganismInfo):
    def __init__(self, id, relative_position, is_alive, is_visible = True):
        super().__init__(id, relative_position, is_alive, is_visible)
        self._last_seen_position = relative_position


    def lost_sighting(self):
        self._relative_position = None
        self._is_visible = False


    def got_sighting(self, position: Position):
        self._relative_position = position
        self._last_seen_position = position
        self._is_visible = True




    @property
    def last_seen_position(self):
        return self._relative_position
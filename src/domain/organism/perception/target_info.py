from domain.components.position import Position
from domain.organism.organism_id import OrganismID



class TargetInfo:
    def __init__(self, id: OrganismID, position:Position, offset: tuple[int,int], is_alive):
        self._id = id
        self._position = position
        self._last_seen_position = position
        self._is_alive = is_alive
        self._is_visible = True
        self._offset = 0,0

    def update(self, position: Position | None = None, offset: tuple[int, int] = None) -> None:
        if position is None:
            self._lost_sighting()
        else:
            self._got_sighting(position, offset)


    def _lost_sighting(self):
        self._is_visible = False
        self._position = None

    def _got_sighting(self, positon: Position, offset: tuple[int,int]):
        self._is_visible = True
        self._position = positon
        self._last_seen_position = positon
        self._offset = offset


    @property
    def id(self):
        return self._id

    @property
    def position(self):
        return self._position

    @property
    def last_seen_position(self):
        return self._last_seen_position

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def offset(self) -> tuple[int,int]:
        return self._offset

    @property
    def is_visible(self):
        return self._is_visible



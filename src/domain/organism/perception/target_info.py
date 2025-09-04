from domain.components.position import Position
from domain.organism.organism_id import OrganismID



class TargetInfo:
    def __init__(self, id: OrganismID, relative_position:Position, is_alive):
        self._kind = id.kind
        self._id = id.id
        self._relative_position = relative_position
        self._last_seen_position = relative_position
        self._is_alive = is_alive
        self._is_visible = True

    def update(self, position: Position | None = None):
        if position is None:
            self._lost_sighting()
        else:
            self._got_sighting(position)


    def _lost_sighting(self):
        self._is_visible = False
        self._relative_position = None

    def _got_sighting(self, positon: Position):
        self._is_visible = True
        self._relative_position = positon
        self._last_seen_position = positon

    @property
    def kind(self):
        return self._kind

    @property
    def id(self):
        return self._id

    @property
    def relative_position(self):
        return self._relative_position

    @property
    def last_seen_position(self):
        return self._last_seen_position

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def is_visible(self):
        return self._is_visible



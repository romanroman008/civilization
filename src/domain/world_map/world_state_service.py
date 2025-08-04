from collections import defaultdict
from typing import Dict, Set, Optional, Sequence

from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.organism.instances.human import Human
from domain.organism.instances.organism import Organism
from domain.organism.organism_id import OrganismID


class WorldStateService:
    def __init__(self):
        self._organism_index: Dict[OrganismID, Organism] = {}
        self._organism_positions: Dict[Organism, Position] = {}
        self._position_organisms: Dict[tuple[int, int], Set[Organism]] = defaultdict(set)
        self._move_targets: Set[tuple[int, int]] = set()

    def register_organism(self, organism: Organism):
        pos = organism.position
        self._organism_positions[organism] = pos
        self._position_organisms[pos.as_key()].add(organism)
        self._organism_index[organism.id] = organism

    def update_position(self, organism_id: OrganismID, new_position: Position):
        organism = self._organism_index[organism_id]
        old_pos = self._organism_positions.get(organism)
        if old_pos:
            self._position_organisms[(old_pos.x, old_pos.y)].discard(organism)
        self._organism_positions[organism] = new_position
        self._position_organisms[(new_position.x, new_position.y)].add(organism)

    def get_organism_position(self, organism: Organism) -> Position:
        return self._organism_positions.get(organism)

    def get_organism_at_position(self, position: Position) -> Optional[Organism]:
        organisms = self._position_organisms.get(position.as_key())
        if not organisms:
            return None
        return next(iter(organisms))

    def is_occupied(self, position: Position) -> bool:
        return bool(self._position_organisms.get((position.x, position.y)))

    def reserve_position(self, position: Position):
        self._move_targets.add((position.x, position.y))

    def is_reserved(self, position: Position) -> bool:
        return (position.x, position.y) in self._move_targets

    def clear_reservations(self):
        self._move_targets.clear()

    def get_all_renderable(self) -> Sequence[Renderable]:
        return list(self._organism_positions.keys())



    def get_example_agent(self) -> Optional[Human]:
        for organism in self._organism_positions:
            if isinstance(organism, Human):
                return organism
        return None


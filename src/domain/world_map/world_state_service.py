from collections import defaultdict
from typing import Dict, Set, Optional, Sequence, Tuple, Iterator

from domain.components.position import Position


from domain.organism.instances.human import Human

from domain.organism.instances.organism import Organism

from domain.organism.organism_id import OrganismID
from shared.id_registry import IdRegistry


class WorldStateService:
    def __init__(self, id_registry: IdRegistry, world_width:int, world_height:int):
        self._id_registry = id_registry

        self._id_to_organism: Dict[OrganismID, Organism] = {}

        self._occupied: Dict[Position, OrganismID] = {}
        self._reserved: Dict[Position, OrganismID] = {}
        self._organisms_to_occupied: Dict[OrganismID, Position] = {}
        self._organisms_to_reserved: Dict[OrganismID, Position] = {}

        self._world_width = world_width
        self._world_height = world_height


    def register_organism(self, organism: Organism):
        organism_id = organism.id
        position = organism.position
        self._organisms_to_occupied[organism_id] = position
        self._occupied[position] = organism_id
        self._id_to_organism[organism_id] = organism

    def get_organism_by_id(self, organism_id: OrganismID) -> Optional[Organism]:
        return self._id_to_organism[organism_id]


    def notify_animal_movement_start(self, organism_id: OrganismID, target_position: Position):
        self._reserved[target_position] = organism_id
        self._organisms_to_reserved[organism_id] = target_position


    def notify_animal_movement_end(self, organism_id: OrganismID):
        prev_position = self._organisms_to_occupied[organism_id]
        reserved_position = self._organisms_to_reserved.pop(organism_id)
        self._organisms_to_occupied[organism_id] = reserved_position
        self._occupied[reserved_position] = organism_id

        del self._occupied[prev_position]
        del self._reserved[reserved_position]


    def get_organism_position(self, organism_id: OrganismID) -> Optional[Position]:
        return self._organisms_to_occupied.get(organism_id)


    def get_organism_at_position(self, position: Position) -> Optional[Organism]:
        organism_id = self._occupied.get(position)
        if not organism_id:
            return None
        return self._id_to_organism[organism_id]


    def get_organisms_at_positions(self, positions: list[Position]):
        positions_organisms = self._occupied
        organisms = []
        for position in positions:
            organism = positions_organisms.get(position)
            if organism:
                organisms.append(organism)
        return organisms


    def is_occupied(self, position: Position) -> bool:
        if position in self._occupied:
            return True
        return False

    def is_reserved(self, position: Position) -> bool:
        if position in self._reserved:
            return True
        return False

    def get_all_organisms(self) -> list[Organism]:
        return [self._id_to_organism[oid] for oid in self._organisms_to_occupied]


    def get_organisms_in_viewport(self, start_x: int, end_x: int, start_y: int, end_y: int) -> Iterator[Organism]:
        end_x = min(end_x + 1, self._world_width)
        end_y = min(end_y + 1, self._world_height)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                organism = self.get_organism_at_position(Position(x, y))
                if not organism:
                    continue
                yield organism


    def get_example_agent(self) -> Optional[Human]:
        for organism in self._organisms_to_occupied:
            if isinstance(organism, Human):
                return organism
        return None



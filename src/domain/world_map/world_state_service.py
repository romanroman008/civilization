from collections import defaultdict
from typing import Dict, Set, Optional, Sequence, Tuple

from domain.components.position import Position
from domain.components.renderable import Renderable
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human

from domain.organism.instances.organism import Organism

from domain.organism.organism_id import OrganismID
from shared.id_registry import IdRegistry


class WorldStateService:
    def __init__(self, id_registry: IdRegistry):
        self._id_registry = id_registry

        self._organism_index: Dict[OrganismID, Organism] = {}
        self._organism_positions: Dict[Organism, Position] = {}
        self._position_organisms: Dict[Position, Set[Organism]] = defaultdict(set)
        self._move_targets: Set[tuple[int, int]] = set()

        self._moving_animals: Dict[OrganismID, tuple[Position, Position]] = {}


    def register_organism(self, organism: Organism):
        pos = organism.position
        self._organism_positions[organism] = pos
        self._position_organisms[pos].add(organism)
        self._organism_index[organism.id] = organism

    def get_organism_by_id(self, organism_id: OrganismID) -> Optional[Organism]:
        return self._organism_index[organism_id]


    def notify_animal_movement_start(self, animal: Organism, target_position: Position):
        self._moving_animals[animal.id] = animal.position, target_position
        self._move_targets.add((target_position.x, target_position.y))


    def notify_animal_movement_end(self, animal: Organism):
        prev_pos, act_pos = self._moving_animals[animal.id]
        del self._moving_animals[animal.id]
        self._move_targets.discard((act_pos.x, act_pos.y))
        self._position_organisms[prev_pos].discard(animal)
        self._organism_positions[animal] = act_pos
        self._position_organisms[act_pos].add(animal)



    def get_organism_position(self, organism: Organism) -> Position:
        return self._organism_positions.get(organism)

    def get_organism_at_position(self, position: Position) -> Optional[Organism]:
        organisms = self._position_organisms.get(position)
        if not organisms:
            return None
        return next(iter(organisms))

    def get_organisms_at_positions(self, positions: list[Position]):
        positions_organisms = self._position_organisms
        organisms = []
        for position in positions:
            organism = positions_organisms.get(position)
            if organism:
                organisms.append(organism)
        return organisms


    def is_occupied(self, position: Position) -> bool:
        return bool(self._position_organisms.get(position))

    def reserve_position(self, position: Position):
        self._move_targets.add((position.x, position.y))

    def is_reserved(self, position: tuple[int,int]) -> bool:
        return (position[0], position[1]) in self._move_targets

    def remove_reservation(self, position: Position):
        self._move_targets.discard((position.x, position.y))


    def get_all_organisms(self) -> Sequence[Organism]:
        return list(self._organism_positions.keys())

    def get_example_agent(self) -> Optional[Human]:
        for organism in self._organism_positions:
            if isinstance(organism, Human):
                return organism
        return None

    def get_all_occupied(self) -> set[Position]:
        return {pos for pos, organisms in self._position_organisms.items() if organisms}

    def get_all_reserved(self) -> set[tuple[int, int]]:
        return self._move_targets



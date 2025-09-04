from typing import Protocol

from domain.components.terrain import Terrain
from domain.organism.organism_id import OrganismID


class WorldInteractionsValidatorProtocol(Protocol):
    def get_organisms_distance(self, organism_a_id:OrganismID, organism_b_id:OrganismID): pass
    def is_position_allowed(self, position, allowed_terrains: set[Terrain]|None = None) -> bool: pass
    def is_organism_alive(self, organism_id: OrganismID) -> bool: pass
    def is_kill_allowed(self, killer_id: OrganismID, victim_id: OrganismID) -> bool: pass
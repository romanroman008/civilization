from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.instances.organism import Organism
from domain.organism.organism_id import OrganismID
from domain.world_map.world_interactions_validator_protocol import WorldInteractionsValidatorProtocol
from domain.world_map.world_map import WorldMap
from domain.world_map.world_state_service import WorldStateService


class WorldInteractionsValidator(WorldInteractionsValidatorProtocol):
    def __init__(self,
                 world_map: WorldMap,
                 world_state_service: WorldStateService):
        self._world_map = world_map
        self._world_state_service = world_state_service


    def _get_organism_by_id(self, organism_id: OrganismID) -> Organism:
        organism = self._world_state_service.get_organism_by_id(organism_id)
        if not organism:
            raise ValueError(f"Organism {organism_id} not found")
        return organism

    def get_organisms_distance(self, organism_a_id: OrganismID, organism_b_id: OrganismID) -> int:
        organism_a = self._get_organism_by_id(organism_a_id)
        organism_b = self._get_organism_by_id(organism_b_id)
        return organism_a.position.distance_to(organism_b.position)

    def is_position_allowed(self, position: tuple[int,int], allowed_terrains: set[Terrain] = None) -> bool:
        if not allowed_terrains:
            return (
                not self._world_state_service.is_occupied(position)
                and not self._world_state_service.is_reserved(position)
            )
        else:
            return (
                self._world_map.is_position_allowed(position, allowed_terrains)
                and not  self._world_state_service.is_occupied(position)
                and not self._world_state_service.is_reserved(position)
            )

    def is_organism_alive(self, organism_id):
        return self._get_organism_by_id(organism_id).is_alive

    def is_kill_allowed(self, killer_id: OrganismID, victim_id: OrganismID) -> bool:
        killer = self._get_organism_by_id(killer_id)
        victim = self._get_organism_by_id(victim_id)

        if not killer.is_alive or not victim.is_alive:
            return False



        return True














from abc import abstractmethod

from domain.components.position import Position
from domain.organism.instances.organism import Organism
from domain.organism.prefabs.organism_prefab import OrganismPrefab


class OrganismFactory:
    @abstractmethod
    def create(self, prefab: OrganismPrefab, position: Position) -> Organism: pass

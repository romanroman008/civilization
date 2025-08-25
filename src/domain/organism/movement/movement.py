from abc import ABC, abstractmethod

from domain.components.direction import Direction
from domain.organism.movement.transform import Transform



class Movement(ABC):
    def __init__(self, transform: Transform):
        self._transform: Transform = transform

    @abstractmethod
    def move(self, target_direction: Direction):
        ...




from abc import ABC, abstractmethod


from domain.components.direction import Direction

from domain.organism.transform.transform_readonly import TransformReadOnly
from domain.organism.transform.transform_writer import TransformWriter


class Movement(ABC):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly):
        self._transform_writer: TransformWriter = transform_writer
        self._transform_readonly: TransformReadOnly = transform_readonly


    @abstractmethod
    def move(self, target_direction: Direction):
        ...


from abc import ABC, abstractmethod


from domain.components.direction import Direction
from domain.organism.transform.transform import TransformWriter, TransformReadOnly


class Movement(ABC):
    def __init__(self, transform_writer: TransformWriter, transform_readonly: TransformReadOnly):
        self._transform_writer: TransformWriter = transform_writer
        self._transform_readonly: TransformReadOnly = transform_readonly


    @abstractmethod
    def move(self, target_direction: Direction):
        ...

    @abstractmethod
    def tick(self):
        ...


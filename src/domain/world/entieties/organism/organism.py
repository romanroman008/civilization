from abc import ABC, abstractmethod
from asyncio import Lock
from dataclasses import dataclass, field
from typing import Optional

from domain.world.entieties.direction import Direction
from domain.world.entieties.position import Position



@dataclass
class Organism(ABC):
    _name: str
    _allowed_terrains: set
    _block_radius: int = 0
    _position: Optional[Position] = None
    _target_position: Optional[Position] = None
    _rotation: int = 0
    _target_rotation: int = 0
    _offset_x: float = 0.0
    _offset_y: float = 0.0

    _facing: Direction = Direction.BOT
    target_facing: Direction = Direction.BOT

    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    isMoving: bool = False

    @property
    def lock(self):
        return self._lock


    @abstractmethod
    def tick(self):
        ...

    @property
    def name(self) -> str:
        return self._name

    @property
    def allowed_terrains(self) -> set:
        return self._allowed_terrains

    @property
    def sprite_key(self) -> str:
        return self._name

    @property
    def block_radius(self) -> int:
        return self._block_radius

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position):
        self._position = value

    @property
    def target_position(self) -> Position:
        return self._target_position

    @target_position.setter
    def target_position(self, value: Position):
        self._target_position = value

    @property
    def rotation(self) -> float:
        return self._rotation

    @property
    def target_rotation(self) -> int:
        return self._target_rotation

    @target_rotation.setter
    def target_rotation(self, value:int):
        self._target_rotation = value

    @property
    def offset(self) -> tuple[float, float]:
        return self._offset_x, self._offset_y

    @property
    def facing(self) -> Direction:
        return self._facing


    def rotate(self, rotation: int):
       self._rotation = (self._rotation + rotation + 180) % 360 - 180

       direction_by_angle = {
           0: Direction.BOT,
           90: Direction.LEFT,
           -180: Direction.TOP,
           -90: Direction.RIGHT,
       }
       if self._rotation in direction_by_angle:
        self._facing = direction_by_angle[self._rotation]


    def move_offset_x(self, x:float):
        self._offset_x = round((self._offset_x + x), 3)

    def move_offset_y(self, y:float):
        self._offset_y = round((self._offset_y + y), 3)

    def reset_rotation(self):
        self._rotation = 0

    def reset_offset(self):
        self._offset_x = 0
        self._offset_y = 0






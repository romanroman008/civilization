from dataclasses import dataclass
from typing import Protocol

from domain.components.position import Position


class OrganismInfo(Protocol):
    id: int
    position: Position
    is_visible: bool
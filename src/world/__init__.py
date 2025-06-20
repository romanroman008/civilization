from dataclasses import dataclass
from typing import List

from view.TileView import TileView


@dataclass
class ChunkView:
    x: int
    y: int
    tiles: List[TileView]
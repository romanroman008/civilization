from typing import List

import numpy as np


from infrastructure.Chunk import Chunk


class WorldMap:
    def __init__(self, tensor: np.ndarray):
        self._tensor = tensor

    def get_chunk(self, chunk_x: int, chunk_y: int) -> Chunk:
        pass





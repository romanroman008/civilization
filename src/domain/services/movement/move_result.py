from enum import Enum


class MoveResult(Enum):
    SUCCESS = "success"
    RESERVED = "reserved"
    OCCUPIED = "occupied"
    OUT_OF_BOUNDS = "out_of_bounds"
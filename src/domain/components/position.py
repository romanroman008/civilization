from typing import NamedTuple

class Position(NamedTuple):
    x: int
    y: int


    def distance_to(self, other: "Position") -> int:
        ox, oy = other
        return abs(self.x - ox) + abs(self.y - oy)  # Manhattan

    def __add__(self, other: "Position") -> "Position":
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, k: int) -> "Position":
        if not isinstance(k, int):
            return NotImplemented
        return Position(self.x * k, self.y * k)

    __rmul__ = __mul__

    def neighbors(self, diagonals: bool = False) -> list["Position"]:
        dirs = DIRECTIONS_8 if diagonals else DIRECTIONS_4
        x, y = self.x, self.y
        return [Position(x + d.x, y + d.y) for d in dirs]

DIRECTIONS_4: tuple["Position", ...] = (
    Position(0, -1), Position(0, 1), Position(-1, 0), Position(1, 0)
)
DIRECTIONS_8: tuple["Position", ...] = DIRECTIONS_4 + (
    Position(-1, -1), Position(1, -1), Position(-1, 1), Position(1, 1)
)



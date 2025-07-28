from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    x: int
    y: int

    def distance_to(self, other: "Position") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)  # Manhattan

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Position":
        return Position(self.x * other, self.y * other)

    # def equals(self, other: object) -> bool:
    #     if not isinstance(other, Position):
    #         return False
    #     return self.x == other.x and self.y == other.y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def neighbors(self, diagonals: bool = False) -> list["Position"]:
        directions = [
            Position(0, -1), Position(0, 1),
            Position(-1, 0), Position(1, 0)
        ]
        if diagonals:
            directions += [
                Position(-1, -1), Position(1, -1),
                Position(-1, 1), Position(1, 1)
            ]
        return [self + d for d in directions]

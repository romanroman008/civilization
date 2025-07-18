import pytest

from domain.world.entieties.position import Position


class TestPositionDistance:
    def test_distance_to_self_is_zero(self):
        p = Position(5, 7)
        assert p.distance_to(p) == 0

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (Position(0, 0), Position(0, 0), 0),
            (Position(1, 1), Position(2, 3), 3),
            (Position(-2, -2), Position(2, 2), 8),
        ],
    )
    def test_manhattan_distance_between_points(self, a, b, expected):
        assert a.distance_to(b) == expected
        assert b.distance_to(a) == expected  # symmetry


class TestPositionAddition:
    def test_add_two_positions_returns_new_position(self):
        a = Position(2, 3)
        b = Position(4, -1)
        result = a + b

        assert isinstance(result, Position)
        assert result.x == 6
        assert result.y == 2

    def test_addition_is_not_in_place(self):
        a = Position(1, 1)
        b = Position(2, 2)
        _ = a + b
        assert a == Position(1, 1)  # original unchanged


class TestPositionNeighbors:
    def test_cardinal_neighbors(self):
        p = Position(0, 0)
        expected = {
            (0, -1), (0, 1),
            (-1, 0), (1, 0)
        }
        neighbors = {(n.x, n.y) for n in p.neighbors()}
        assert neighbors == expected

    def test_all_neighbors_with_diagonals(self):
        p = Position(0, 0)
        expected = {
            (0, -1), (0, 1),
            (-1, 0), (1, 0),
            (-1, -1), (1, -1),
            (-1, 1), (1, 1)
        }
        neighbors = {(n.x, n.y) for n in p.neighbors(diagonals=True)}
        assert neighbors == expected


class TestPositionEqualityAndHash:
    def test_equality_and_hash(self):
        a = Position(2, 3)
        b = Position(2, 3)
        c = Position(3, 2)

        assert a == b
        assert a != c
        assert hash(a) == hash(b)

    def test_position_as_dict_key(self):
        position_map = {
            Position(1, 1): "A",
            Position(2, 2): "B"
        }
        assert position_map[Position(1, 1)] == "A"
        assert position_map.get(Position(2, 2)) == "B"
        assert position_map.get(Position(3, 3)) is None

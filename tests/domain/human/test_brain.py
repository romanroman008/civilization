
from unittest.mock import MagicMock


from domain.components.position import Position
from domain.components.direction import Direction
from domain.components.terrain import Terrain

from domain.human.brain import Brain
from domain.human.perception.percived_object import PerceivedObject


def make_brain() -> Brain:
    return Brain(field_of_view=MagicMock(), vitals=MagicMock())


def make_obj(x: int, y: int, terrain: Terrain = Terrain.GRASS) -> PerceivedObject:
    return PerceivedObject(
        relative_position=Position(x, y),
        terrain=terrain,
        organism_info=None
    )


def test_straight_line_path():
    brain = make_brain()
    brain._perceived_objects = [
        make_obj(0, 0),
        make_obj(0, 1)
    ]

    path = brain.find_shortest_path(Position(0, 0), Position(0, 1))

    assert path == [Direction.BOT]


def test_turning_path():
    brain = make_brain()
    brain._perceived_objects = [
        make_obj(0, 0),
        make_obj(1, 0),
        make_obj(1, 1)
    ]

    path = brain.find_shortest_path(Position(0, 0), Position(1, 1))

    assert path in [
        [Direction.RIGHT, Direction.BOT],
        [Direction.BOT, Direction.RIGHT]
    ]


def test_unreachable_goal():
    brain = make_brain()
    brain._perceived_objects = [
        make_obj(0, 0),
        make_obj(0, 1, terrain=Terrain.WATER)
    ]

    path = brain.find_shortest_path(Position(0, 0), Position(0, 1))

    assert path is None


def test_surrounded_by_water():
    brain = make_brain()
    brain._perceived_objects = [
        make_obj(0, 0),
        make_obj(0, 1, terrain=Terrain.WATER),
        make_obj(1, 0, terrain=Terrain.WATER),
        make_obj(0, -1, terrain=Terrain.WATER),
        make_obj(-1, 0, terrain=Terrain.WATER),
    ]

    path = brain.find_shortest_path(Position(0, 0), Position(1, 1))

    assert path is None


def test_shortest_path_around_wall():
    brain = make_brain()
    brain._perceived_objects = [
        make_obj(0, 0),
        make_obj(0, 1, terrain=Terrain.WATER),
        make_obj(1, 0),
        make_obj(1, 1),
        make_obj(0, 2),
        make_obj(1, 2),

    ]

    path = brain.find_shortest_path(Position(0, 0), Position(0, 2))

    assert path == [Direction.RIGHT,Direction.BOT, Direction.BOT, Direction.LEFT]


def test_small_map():
    brain = make_brain()
    brain._perceived_objects = [
        make_obj(-1, -1),
        make_obj(-1, 0),
        make_obj(-1, 1),
        make_obj(-1, 2),

        make_obj(0, -1),
        make_obj(0, 0),
        make_obj(0, 1, terrain=Terrain.WATER),
        make_obj(0, 2),

        make_obj(1, -1),
        make_obj(1, 0, terrain=Terrain.WATER),
        make_obj(1, 1),
        make_obj(1, 2),

        make_obj(2, -1),
        make_obj(2, 0, terrain=Terrain.WATER),
        make_obj(2, 1),
        make_obj(2, 2),

        make_obj(3, -1),
        make_obj(3, 0),
        make_obj(3, 1),
        make_obj(3, 2),

    ]

    path = brain.find_shortest_path(Position(0, 0), Position(2, 2))

    assert path == [Direction.LEFT, Direction.BOT, Direction.BOT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT]

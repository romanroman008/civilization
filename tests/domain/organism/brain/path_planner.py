import types
from collections import deque
from typing import Dict, Tuple

import pytest

from domain.components.direction import Direction
from domain.components.terrain import Terrain
from domain.organism.brain.path_planner import PathPlanner
from domain.organism.perception.vision import Vision
from domain.organism.transform.transform import TransformReadOnly



# --- Pomocnicze stuby minimalne ---

# zamiast: class _DummyTransform(TransformReadOnly):
class _DummyTransform:
    __slots__ = ("position",)

    def __init__(self, x: int, y: int):
        # użyj Twojej klasy Position
        from domain.components.position import Position
        self.position = Position(x, y)


class _DummyVision(Vision):
    """Nie będzie używana w testach (stub), bo monkeypatchujemy _get_possible_move_neighbours."""
    def __init__(self): pass


# Fabryka sąsiadów: zwraca metodę zgodną z sygnaturą _get_possible_move_neighbours
# Sąsiedzi to tylko te kafle, które są w zbiorze 'passable'.
def neighbours_factory(passable: set[Tuple[int, int]]):
    vecs = {
        Direction.RIGHT: (1, 0),
        Direction.LEFT:  (-1, 0),
        Direction.TOP:   (0, -1),
        Direction.BOT:   (0, 1),
    }
    def _neigh(self, current_pos: Tuple[int, int]) -> Dict[Direction, Tuple[int, int]]:
        x, y = current_pos
        out: Dict[Direction, Tuple[int, int]] = {}
        for d, (dx, dy) in vecs.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in passable:
                out[d] = (nx, ny)
        return out
    return _neigh


def _bind_neighbours(planner: PathPlanner, passable: set[Tuple[int, int]]):
    """Podpina metodę _get_possible_move_neighbours do instancji PathPlanner."""
    method = neighbours_factory(passable)
    planner._get_possible_move_neighbours = types.MethodType(method, planner)


# --- TESTY ---

def test_returns_empty_path_when_start_equals_goal(monkeypatch):
    start = (2, 3)
    goal = (2, 3)
    transform = _DummyTransform(*start)
    planner = PathPlanner(vision=_DummyVision(), transform=transform, available_terrains={Terrain.GRASS})
    # dowolny zbiór przejść – nieistotny, i tak zwróci od razu
    _bind_neighbours(planner, passable={start})

    path = planner.find_shortest_path(goal)
    assert path == [], "Gdy start == goal, ścieżka powinna być pusta listą."


def test_finds_straight_right_path(monkeypatch):
    start = (0, 0)
    goal = (2, 0)
    passable = {(0, 0), (1, 0), (2, 0)}

    planner = PathPlanner(_DummyVision(), _DummyTransform(*start), {Terrain.GRASS})
    _bind_neighbours(planner, passable)

    path = planner.find_shortest_path(goal)
    assert path is not None
    assert path == [Direction.RIGHT, Direction.RIGHT]


def test_finds_shortest_with_turn(monkeypatch):
    # Mapa:
    # (0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2)  (zakręt w dół)
    start = (0, 0)
    goal = (2, 2)
    passable = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}

    planner = PathPlanner(_DummyVision(), _DummyTransform(*start), {Terrain.GRASS})
    _bind_neighbours(planner, passable)

    path = planner.find_shortest_path(goal)
    assert path is not None
    assert path == [Direction.RIGHT, Direction.RIGHT, Direction.BOT, Direction.BOT]


def test_no_path_returns_none(monkeypatch):
    start = (0, 0)
    goal = (1, 0)
    passable = {(0, 0)}  # brak przejścia do (1,0)

    planner = PathPlanner(_DummyVision(), _DummyTransform(*start), {Terrain.GRASS})
    _bind_neighbours(planner, passable)

    path = planner.find_shortest_path(goal)
    assert path is None

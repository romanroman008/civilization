from unittest.mock import Mock

import pytest

from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.world_map.tile import Tile
from domain.world_map.world_map import WorldMap


@pytest.fixture
def tiles():
    return [
        Tile(_id=1, _x=0, _y=0, _terrain=Terrain.WATER),
        Tile(_id=2, _x=1, _y=0, _terrain=Terrain.WATER),
        Tile(_id=3, _x=2, _y=0, _terrain=Terrain.WATER),
        Tile(_id=4, _x=3, _y=0, _terrain=Terrain.WATER),
        Tile(_id=5, _x=0, _y=1, _terrain=Terrain.WATER),
        Tile(_id=6, _x=1, _y=1, _terrain=Terrain.WATER),
        Tile(_id=7, _x=2, _y=1, _terrain=Terrain.GRASS),
        Tile(_id=8, _x=3, _y=1, _terrain=Terrain.GRASS),
        Tile(_id=9, _x=0, _y=2, _terrain=Terrain.GRASS),
        Tile(_id=10, _x=1, _y=2, _terrain=Terrain.WATER),
        Tile(_id=11, _x=2, _y=2, _terrain=Terrain.GRASS),
        Tile(_id=12, _x=3, _y=2, _terrain=Terrain.GRASS)
    ]


@pytest.fixture
def world(tiles):
    return WorldMap(_id=42, _name="TestWorld", _width=4, _height=3, _tiles=tiles)


def test_properties(world):
    assert world.id == 42
    assert world.name == "TestWorld"
    assert world.width == 4 and world.height == 3
    assert isinstance(world.tiles, tuple)
    assert world.organisms == ()



@pytest.mark.parametrize("x,y", [
    (0,0),
    (1,0),
    (2,0),
    (3,0),
    (0,1),
    (1,1),
    (2,1),
    (3,1),
    (0,2),
    (1,2),
    (2,2),
    (3,2)
])
def test_get_tiles_by_coords(world, tiles, x, y):
    tile = world.get_tile_by_coords(x,y)
    assert tile.x == x
    assert tile.y == y


@pytest.mark.parametrize("x,y", [
    (0,-3),
    (-1,0),
    (-1,-4),
    (2,6),
    (4,2),
    (99,99)
])
def test_get_tile_by_invalid_coords(world, tiles, x, y):
    with pytest.raises(KeyError):
        world.get_tile_by_coords(x,y)


def test_get_tile_by_position(world):
    pos = Position(2, 1)
    # powinno delegować do get_tile_by_coords
    assert world.get_tile_by_position(pos) is world.get_tile_by_coords(2, 1)


def test_is_tile_and_position_occupied(world):
    # początkowo nic nie jest zajęte
    assert not world.is_tile_occupied(0, 0)
    assert not world.is_position_occupied(Position(0, 0))

    # zasymulujmy zajęcie kafla (np. przez dodanie organizmu)
    tile = world.get_tile_by_coords(1, 1)
    dummy_org = Mock()
    tile.add_organism(dummy_org)

    assert world.is_tile_occupied(1, 1)
    assert world.is_position_occupied(Position(1, 1))


@pytest.mark.parametrize("x,y,expected", [
    (0, 0, True),
    (3, 2, True),
    (4, 0, False),  # x == width
    (0, 3, False),  # y == height
    (-1, 0, False),
    (0, -1, False),
])
def test_is_position_in_bounds(world, x, y, expected):
    assert world.is_position_in_bounds(Position(x, y)) is expected


@pytest.mark.parametrize("x,y,occupy,expected", [
    (0, 0, False, True),   # w granicach i wolne
    (1, 1, True, False),   # w granicach, ale zajęte
    (3, 2, False, True),
    (4, 0, False, False),  # poza granicami
])
def test_is_position_available(world, tiles, x, y, occupy, expected):
    pos = Position(x, y)
    if occupy and world.is_position_in_bounds(pos):
        # zajmujemy kafel przez dodanie organizmu
        world.get_tile_by_coords(x, y).add_organism(Mock())
    assert world.is_position_available(pos) is expected


def test_add_organism_appends_and_marks_tile(world):
    # przygotuj dummy-organizm z pozycją
    dummy = Mock()
    dummy.position = Position(3, 2)
    target = world.get_tile_by_coords(3, 2)

    # przed dodaniem nic nie ma
    assert not target._organisms
    assert world.organisms == ()

    world.add_organism(dummy)

    # organizm trafia do kolekcji WorldMap
    assert dummy in world.organisms
    # i kafel rzeczywiście go otrzymuje
    assert dummy in target._organisms


def test_get_all_renderable_includes_tiles_then_organisms(world, tiles):
    # gdy nie ma organizmów → tylko kafle
    renderable = world.get_all_renderable()
    assert list(renderable[:len(tiles)]) == list(world.tiles)
    assert list(renderable[len(tiles):]) == []

    # dodajmy dwa organizmy
    org1 = Mock(position=Position(0, 0))
    org2 = Mock(position=Position(1, 0))
    world.add_organism(org1)
    world.add_organism(org2)

    renderable2 = world.get_all_renderable()
    # pierwsza część dalej to wszystkie tile
    assert list(renderable2[:len(tiles)]) == list(world.tiles)
    # po nich dokładnie nasze dwa organizmy, w kolejności dodania
    assert renderable2[len(tiles):] == [org1, org2]

import pytest
from unittest.mock import Mock

import domain.world.services.generators.plants_generator as pg_mod
from domain.world.services.generators.plants_generator import PlantsGenerator
from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain


class FakePlant:
    def __init__(self, name, allowed_terrains, block_radius=None):
        # Accepts two or three args to match both prototype and instantiation
        self.name = name
        self.allowed_terrains = allowed_terrains
        self.block_radius = block_radius
        self.position = None


@pytest.fixture(autouse=True)
def patch_Plant(monkeypatch):
    """
    Replace Plant in the module under test with FakePlant
    so we can inspect created instances.
    """
    monkeypatch.setattr(pg_mod, 'Plant', FakePlant)


@pytest.fixture
def dummy_world():
    """
    A fake world that records add_organism calls
    and has predictable dimensions and terrain.
    """
    w = Mock()
    w.width = 5
    w.height = 5
    # always return a tile whose terrain is GRASS
    w.get_tile_by_position = lambda pos: Mock(terrain=Terrain.GRASS)
    w.add_organism = Mock()
    return w


@pytest.fixture
def simple_distribution():
    """
    One species at 40% fraction, block_radius=1, allowed only on GRASS.
    """
    prototype = FakePlant("Fern", [Terrain.GRASS], block_radius=1)
    return [(prototype, 0.4)]


def test_generate_plants_sets_world_and_returns_same_instance(dummy_world, simple_distribution):
    gen = PlantsGenerator(count=10, species_distribution=simple_distribution)
    # patch internals to make it deterministic
    all_positions = [Position(x, x) for x in range(5)]
    gen._get_valid_positions = lambda h, w, p: all_positions
    gen._get_random_positions_with_blocking = lambda c, p, n: c[:n]

    returned = gen.generate_plants(dummy_world)
    assert returned is dummy_world
    assert gen.world is dummy_world


def test_generate_plants_adds_expected_number_of_plants_when_positions_sufficient(dummy_world, simple_distribution):
    gen = PlantsGenerator(count=10, species_distribution=simple_distribution)
    # valid positions list of length 5
    positions = [Position(x, 0) for x in range(5)]
    gen._get_valid_positions = lambda h, w, p: positions
    # pick first amount = int(0.4*10) = 4 positions
    gen._get_random_positions_with_blocking = lambda c, p, n: c[:n]

    gen.generate_plants(dummy_world)
    assert dummy_world.add_organism.call_count == 4

    for idx, call in enumerate(dummy_world.add_organism.call_args_list):
        plant = call[0][0]
        assert isinstance(plant, FakePlant)
        assert plant.name == simple_distribution[0][0].name
        assert plant.allowed_terrains == simple_distribution[0][0].allowed_terrains
        assert plant.position == positions[idx]


def test_generate_plants_adds_all_available_plants_when_positions_insufficient(dummy_world, simple_distribution):
    gen = PlantsGenerator(count=10, species_distribution=simple_distribution)
    # only 2 valid positions but amount = 4
    positions = [Position(0, 0), Position(1, 1)]
    gen._get_valid_positions = lambda h, w, p: positions
    gen._get_random_positions_with_blocking = lambda c, p, n: c[:n]

    gen.generate_plants(dummy_world)
    assert dummy_world.add_organism.call_count == 2


def test_generate_plants_adds_no_plants_when_no_valid_positions(dummy_world, simple_distribution):
    gen = PlantsGenerator(count=10, species_distribution=simple_distribution)
    gen._get_valid_positions = lambda h, w, p: []
    gen._get_random_positions_with_blocking = lambda c, p, n: c[:n]

    gen.generate_plants(dummy_world)
    assert dummy_world.add_organism.call_count == 0

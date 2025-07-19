import numpy as np
import pytest
from unittest.mock import Mock, call

import domain.world.services.generators.world_generator as wg_mod
from domain.world.services.generators.world_generator import WorldGenerator
from domain.world.entieties.world_map import WorldMap

@pytest.fixture
def dummy_logger():
    return Mock(info=Mock())

@pytest.fixture
def dummy_elevation_generator():
    eg = Mock()
    eg.generate_elevation = Mock(side_effect=lambda nx, ny: nx + ny)
    return eg

@pytest.fixture
def dummy_plants_generator():
    pg = Mock()
    pg.generate_plants = Mock(side_effect=lambda w: w)
    return pg

@pytest.fixture
def dummy_animals_generator():
    ag = Mock()
    ag.generate = Mock(side_effect=lambda w: w)
    return ag

@pytest.fixture
def world_generator(dummy_logger,
                    dummy_elevation_generator,
                    dummy_plants_generator,
                    dummy_animals_generator):
    return WorldGenerator(
        logger=dummy_logger,
        elevation_generator=dummy_elevation_generator,
        plants_generator=dummy_plants_generator,
        animals_generator=dummy_animals_generator,
    )

def test__generate_map_array_returns_correct_elevations_and_logs(world_generator, dummy_logger, dummy_elevation_generator):
    arr = world_generator._generate_map_array(width=2, height=3, scale=10)
    assert arr.shape == (3, 2)
    expected = np.array([[0/10 + 0/10, 1/10 + 0/10],
                         [0/10 + 1/10, 1/10 + 1/10],
                         [0/10 + 2/10, 1/10 + 2/10]], dtype=np.float32)
    assert np.allclose(arr, expected)
    assert dummy_logger.info.call_args_list[0] == call("Generating world started ...")
    assert dummy_logger.info.call_args_list[1] == call("Finished generating world")
    calls = [call(x/10, y/10) for y in range(3) for x in range(2)]
    assert dummy_elevation_generator.generate_elevation.call_args_list == calls

def test_create_delegates_to_internal_steps_and_returns_worldmap(monkeypatch, world_generator):
    fake_array = np.array([[0.1]])
    monkeypatch.setattr(world_generator, '_generate_map_array', lambda w, h, s: fake_array)
    # zwracamy obiekt z .x, .y, .id, by WorldMap __post_init__ zadziałało
    fake_tile = Mock(x=0, y=0, id=0)
    monkeypatch.setattr(wg_mod.TileAdapter, 'to_tiles', lambda arr: [fake_tile])
    monkeypatch.setattr(world_generator, '_generate_plants', lambda w: "AFTER_PLANTS")
    monkeypatch.setattr(world_generator, '_generate_animals', lambda w: "AFTER_ANIMALS")

    result = world_generator.create(width=1, height=1, scale=5)
    assert result == "AFTER_ANIMALS"

def test__generate_plants_logs_and_delegates(world_generator, dummy_logger, dummy_plants_generator):
    wm = Mock()
    out = world_generator._generate_plants(wm)
    assert out is wm
    assert dummy_logger.info.call_args_list[-2] == call("Generating plants started ...")
    assert dummy_logger.info.call_args_list[-1] == call("Finished generating plants")
    dummy_plants_generator.generate_plants.assert_called_once_with(wm)

def test__generate_animals_logs_and_delegates(world_generator, dummy_logger, dummy_animals_generator):
    wm = Mock()
    out = world_generator._generate_animals(wm)
    assert out is wm
    assert dummy_logger.info.call_args_list[-2] == call("Generating animals started ...")
    assert dummy_logger.info.call_args_list[-1] == call("Finished generating animals")
    dummy_animals_generator.generate.assert_called_once_with(wm)

@pytest.mark.parametrize("y, height, expected", [
    (0, 10, 1.0),      # top edge
    (5, 10, 0.0),      # center
    (10, 10, 1.0),     # bottom edge
    (2.5, 10, 0.5),    # fractional position
])
def test_normalize_latitude_returns_correct_ratio(world_generator, y, height, expected):
    world_generator.height = height
    norm = world_generator._WorldGenerator__normalize_latitude(y)
    assert pytest.approx(norm, rel=1e-3) == expected

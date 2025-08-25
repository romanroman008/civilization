import pytest
from unittest.mock import Mock

import domain.services.generators.animals_generator as ag_mod
from domain.services.generators import AnimalsGenerator
from domain.components.position import Position
from domain.components.terrain import Terrain

# --- Helpers / Fakes -------------------------------------------------------

class FakeAnimal:
    def __init__(self, name, allowed_terrains):
        self.name = name
        self.allowed_terrains = allowed_terrains
        self.position = None

@pytest.fixture(autouse=True)
def patch_animal(monkeypatch):
    """
    Zastępujemy klasę Animal w module generatora,
    by kontrolować tworzone instancje.
    """
    monkeypatch.setattr(ag_mod, 'Animal', FakeAnimal)


# --- Fixtures --------------------------------------------------------------

@pytest.fixture
def dummy_world():
    """
    Świat, który tylko zbiera wywołania add_organism.
    """
    w = Mock()
    w.add_organism = Mock()
    return w

@pytest.fixture
def simple_distribution():
    """
    Jedna „gatunkowa” dystrybucja: 50% z count.
    """
    specie = FakeAnimal("Wolf", [Terrain.GRASS])
    return [(specie, 0.5)]


# --- Testy metod prywatnych -----------------------------------------------

def test_is_valid_position_returns_true_when_tile_terrain_allowed(monkeypatch):
    generator = AnimalsGenerator(count=0, species_distribution=[])
    # ustawiamy generator.world tak, by get_tile_by_position zwracało kafel z danym terenem
    fake_tile = Mock(terrain=Terrain.GRASS)
    generator.world_facade = Mock(get_tile_by_position=lambda pos: fake_tile)

    pos = Position(1, 2)
    assert generator._is_valid_position(pos, Mock(allowed_terrains=[Terrain.GRASS]))


def test_is_valid_position_returns_false_when_tile_terrain_not_allowed(monkeypatch):
    generator = AnimalsGenerator(count=0, species_distribution=[])
    fake_tile = Mock(terrain=Terrain.WATER)  # niepasujący teren
    generator.world_facade = Mock(get_tile_by_position=lambda pos: fake_tile)

    pos = Position(0, 0)
    assert not generator._is_valid_position(pos, Mock(allowed_terrains=[Terrain.GRASS]))


def test_get_valid_positions_filters_positions_based_on_is_valid(monkeypatch):
    generator = AnimalsGenerator(count=0, species_distribution=[])
    # nadpisujemy _is_valid_position: tylko (0,0) i (1,1) są dopuszczalne
    def fake_is_valid(pos, animal):
        return (pos.x, pos.y) in {(0, 0), (1, 1)}
    generator._is_valid_position = fake_is_valid

    valid = generator._get_valid_positions(height=3, width=3, animal=Mock())
    coords = {(p.x, p.y) for p in valid}
    assert coords == {(0, 0), (1, 1)}


# --- Testy metody generate ------------------------------------------------

def test_generate_returns_same_world_and_sets_world_attribute(dummy_world, simple_distribution, monkeypatch):
    gen = AnimalsGenerator(count=4, species_distribution=simple_distribution)
    # podmieniamy _get_valid_positions i _get_random_positions, by były deterministyczne
    all_positions = [Position(0,0), Position(1,0), Position(0,1)]
    monkeypatch.setattr(gen, '_get_valid_positions', lambda h, w, org: all_positions)
    monkeypatch.setattr(ag_mod, '_get_random_positions', lambda positions, amount: positions[:amount])

    returned = gen.generate(dummy_world)
    assert returned is dummy_world
    # world atrybut został ustawiony
    assert gen.world_facade is dummy_world

def test_generate_calls_add_organism_expected_number_of_times(dummy_world, simple_distribution, monkeypatch):
    # 50% z 6 → int(0.5*6)=3
    gen = AnimalsGenerator(count=6, species_distribution=simple_distribution)
    positions = [Position(0,0), Position(1,0), Position(2,0), Position(3,0)]
    monkeypatch.setattr(gen, '_get_valid_positions', lambda h, w, org: positions)
    monkeypatch.setattr(ag_mod, '_get_random_positions',
                        lambda positions, amount: positions[:amount])

    gen.generate(dummy_world)
    # powinno być dokładnie 3 wywołania add_organism
    assert dummy_world.add_organism.call_count == 3

def test_generate_passes_animals_with_correct_name_and_allowed_terrains(dummy_world, simple_distribution, monkeypatch):
    gen = AnimalsGenerator(count=2, species_distribution=simple_distribution)
    # wymusimy jeden punkt
    pos_list = [Position(9,9)]
    monkeypatch.setattr(gen, '_get_valid_positions', lambda h, w, org: pos_list)
    monkeypatch.setattr(ag_mod, '_get_random_positions',
                        lambda positions, amount: positions)

    gen.generate(dummy_world)
    # wyciągamy stworzone instancje
    calls = dummy_world.add_organism.call_args_list
    assert len(calls) == 1
    animal_passed = calls[0][0][0]
    # powinien to być FakeAnimal z nazwą i allowed_terrains ze simple_distribution
    orig_specie, _ = simple_distribution[0]
    assert isinstance(animal_passed, FakeAnimal)
    assert animal_passed.name == orig_specie.name
    assert animal_passed.allowed_terrains == orig_specie.allowed_terrains
    # a pozycja zgodnie z implementacją:
    assert animal_passed.position == Position(3, 4)

def test_generate_with_no_available_positions_does_not_call_add_organism(dummy_world, simple_distribution, monkeypatch):
    gen = AnimalsGenerator(count=5, species_distribution=simple_distribution)
    monkeypatch.setattr(gen, '_get_valid_positions', lambda h, w, org: [])
    # nawet jeśli sample miałoby coś zwrócić, nie ma żadnej pozycji
    monkeypatch.setattr(ag_mod, '_get_random_positions',
                        lambda positions, amount: positions)

    gen.generate(dummy_world)
    assert dummy_world.add_organism.call_count == 0

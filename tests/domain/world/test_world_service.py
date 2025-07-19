import pytest
from types import SimpleNamespace
from unittest.mock import Mock

from domain.world.entieties.terrain import Terrain
from domain.world.entieties.tile import Tile
from domain.world.entieties.world_map import WorldMap
from domain.world.services.world_service import WorldService
from infrastructure.persistance.models.tiledb import TileDB
from infrastructure.persistance.models.worlddb import WorldDB


@pytest.fixture
def world_generator():
    gen = Mock()
    gen.create = Mock(return_value="WORLD_INSTANCE")
    return gen


@pytest.fixture
def service(world_generator):
    return WorldService(world_generator)


class DummySession:
    def __init__(self):
        self.add = Mock()
        self.commit = Mock()
        self.execute = Mock()


class DummyCM:
    def __init__(self, session):
        self._session = session
    def __enter__(self):
        return self._session
    def __exit__(self, exc_type, exc, tb):
        pass


@pytest.fixture(autouse=True)
def patch_get_session(monkeypatch):
    """
    Podmieniamy get_session na DummyCM, by kontrolować add/commit/execute.
    """
    import domain.world.services.world_service as ws_mod
    session = DummySession()
    monkeypatch.setattr(ws_mod, 'get_session', lambda: DummyCM(session))
    return session


@pytest.fixture
def sample_tiles():
    # 2×2 grid z naprzemiennym TERRAIN
    return [
        Tile(_id=1, _x=0, _y=0, _terrain=Terrain.WATER),
        Tile(_id=2, _x=1, _y=0, _terrain=Terrain.GRASS),
        Tile(_id=3, _x=0, _y=1, _terrain=Terrain.GRASS),
        Tile(_id=4, _x=1, _y=1, _terrain=Terrain.WATER),
    ]


@pytest.fixture
def sample_world_map(sample_tiles):
    return WorldMap(_id=7, _name="SAMPLE", _width=2, _height=2, _tiles=sample_tiles)


def test_create_new_world_calls_generator_with_correct_args(service, world_generator):
    returned = service.create_new_world(10, 20, 3)
    world_generator.create.assert_called_once_with(10, 20, 3)
    assert returned == "WORLD_INSTANCE"


def test_save_world_adds_worlddb_and_commits_session(patch_get_session, service, sample_world_map):
    service.save_world(sample_world_map)

    session = patch_get_session
    session.add.assert_called_once()
    session.commit.assert_called_once()

    added = session.add.call_args[0][0]
    assert isinstance(added, WorldDB)
    # podstawowe pola
    assert added.name == sample_world_map.name
    assert added.width == sample_world_map.width
    assert added.height == sample_world_map.height

    # konwersja kafli
    assert isinstance(added.tiles, list)
    assert all(isinstance(td, TileDB) for td in added.tiles)
    for orig, td in zip(sample_world_map.tiles, added.tiles):
        assert td.x == orig.x
        assert td.y == orig.y
        assert td.terrain == orig.terrain.value


def test_save_world_converts_each_tile_to_tiledb_before_persisting(patch_get_session, service, sample_world_map):
    service.save_world(sample_world_map)

    added = patch_get_session.add.call_args[0][0]
    # oddzielny test na samą konwersję _tile_to_db
    terrains = [td.terrain for td in added.tiles]
    expected = [t.terrain.value for t in sample_world_map.tiles]
    assert terrains == expected


def test_get_world_by_name_raises_value_error_when_not_found(service):
    # w session.execute.scalar_one_or_none() zwracamy None
    stub = Mock()
    stub.scalar_one_or_none.return_value = None
    patch_get_session = DummySession()
    patch_get_session.execute.return_value = stub
    import domain.world.services.world_service as ws_mod
    pytest.MonkeyPatch().setattr(ws_mod, 'get_session', lambda: DummyCM(patch_get_session))

    with pytest.raises(ValueError) as exc:
        service.get_world_by_name("NOPE")
    assert "World with name 'NOPE' not found." in str(exc.value)


def test_get_world_by_name_returns_worldmap_with_expected_properties_when_record_exists(service):
    # przygotowanie „rekordu” ze świata
    tile_db = [
        SimpleNamespace(id=11, x=0, y=0, terrain=Terrain.WATER.value),
        SimpleNamespace(id=12, x=1, y=0, terrain=Terrain.GRASS.value),
    ]
    world_db = SimpleNamespace(id=99, name="FOUND", width=1, height=1, tiles=tile_db)

    session = DummySession()
    stub = Mock()
    stub.scalar_one_or_none.return_value = world_db
    session.execute.return_value = stub
    import domain.world.services.world_service as ws_mod
    pytest.MonkeyPatch().setattr(ws_mod, 'get_session', lambda: DummyCM(session))

    result = service.get_world_by_name("FOUND")
    # podstawowe pola WorldMap
    assert isinstance(result, WorldMap)
    assert result.id == 99
    assert result.name == "FOUND"
    assert result.width == 1
    assert result.height == 1

    # kafle odwzorowane poprawnie
    xs_ys = [(t.x, t.y, t.terrain) for t in result.tiles]
    assert xs_ys == [(0, 0, Terrain.WATER), (1, 0, Terrain.GRASS)]

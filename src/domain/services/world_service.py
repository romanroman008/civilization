from typing import Sequence

from sqlalchemy import select

from domain.components.terrain import Terrain
from domain.world_map.tile import Tile
from domain.world_map.world_map import WorldMap

from domain.services.generators.world_generator import WorldGenerator

from infrastructure.persistance.models.tiledb import TileDB
from infrastructure.persistance.models.worlddb import WorldDB

from infrastructure.persistance.session import get_session


class WorldService:
    def __init__(self, world_generator: WorldGenerator):
        self.world_generator = world_generator

    def create_new_world(self, width, height, scale) -> WorldMap:
        return self.world_generator.create(width, height, scale)

    def save_world(self, world: WorldMap):
        with get_session() as session:
            tiles_db = self._tiles_to_db(world.tiles)
            world_db = WorldDB(
                name=world.name,
                width=world.width,
                height=world.height,
                tiles=tiles_db
            )
            session.add(world_db)
            session.commit()

    def get_world_by_name(self, name: str) -> WorldMap:
        with get_session() as session:
            stmt = select(WorldDB).where(WorldDB.name == name)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                raise ValueError(f"World with name '{name}' not found.")

            tiles = self._db_to_tiles(result.tiles)

            return WorldMap(
                _id=result.id,
                _name=name,
                _width=result.width,
                _height=result.height,
                _tiles=tiles
            )

    def _db_to_tile(self, tile_db: TileDB) -> Tile:
        return Tile(tile_db.id, tile_db.x, tile_db.y, Terrain(tile_db.terrain))

    def _db_to_tiles(self, tiles_db: list[TileDB]) -> list[Tile]:
        return [self._db_to_tile(db) for db in tiles_db]

    def _tiles_to_db(self, tiles: Sequence[Tile]):
        return [self._tile_to_db(tile) for tile in tiles]

    def _tile_to_db(self, tile: Tile) -> TileDB:
        return TileDB(
            x=tile.x,
            y=tile.y,
            terrain=tile.terrain
        )

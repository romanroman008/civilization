import numpy as np
from sqlalchemy import select

from domain.world.entieties.position import Position
from domain.world.entieties.terrain import Terrain
from domain.world.entieties.tile import Tile
from domain.world.entieties.world_map import WorldMap
from domain.world.services import tile_adapter
from domain.world.services.generators.world_generator import WorldGenerator
from domain.world.services.tile_adapter import TileAdapter
from infrastructure.persistance.models.tiledb import TileDB
from infrastructure.persistance.models.worlddb import WorldDB
from infrastructure.persistance.repositories.tile_repository import TileRepository
from infrastructure.persistance.session import get_session


class WorldService:
    def __init__(self,world_generator:WorldGenerator):
        self.world_generator = world_generator


    def create_new_world(self, width, height, scale) -> WorldMap:
        return self.world_generator.create(width, height, scale)


    def save_world(self, world: WorldMap):
        with get_session() as session:
            tiles_db = self._tiles_to_db(world.tiles)
            world_db = WorldDB(
                name = world.name,
                width = world.width,
                height = world.height,
                tiles = tiles_db
            )
            session.add(world_db)
            session.commit()

    def get_world_by_name(self, name:str) -> WorldMap:
        with get_session() as session:
            stmt = select(WorldDB).where(WorldDB.name == name)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                raise ValueError(f"World with name '{name}' not found.")


            tiles = self._db_to_tiles(result.tiles)

            return WorldMap(
                id=result.id,
                name = name,
                width = result.width,
                height = result.height,
                tiles = tiles
            )





    def _db_to_tile(self, tile_db:TileDB) -> Tile:
        return Tile(tile_db.id, tile_db.x,  tile_db.y, False, Terrain(tile_db.terrain))

    def _db_to_tiles(self, tiles_db: list[TileDB]) -> list[Tile]:
        return [self._db_to_tile(db) for db in tiles_db]

    def _tiles_to_db(self, tiles:list[Tile]):
        return [self._tile_to_db(tile) for tile in tiles]

    def _tile_to_db(self, tile:Tile) -> TileDB:
        return TileDB(
                    x=tile.x,
                    y=tile.y,
                    terrain=tile.terrain
                )










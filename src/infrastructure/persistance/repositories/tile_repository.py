from typing import List, Optional

from sqlalchemy import select

from sqlalchemy.orm import Session

from infrastructure.persistance.models.tiledb import TileDB


class TileRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, tile: TileDB) -> None:
        self.session.add(tile)

    def add_many(self, tiles: List[TileDB]) -> None:
        self.session.add_all(tiles)

    def get_by_coordinates(self, x: int, y: int) -> Optional[TileDB]:
        return self.session.query(TileDB).filter_by(x=x, y=y).first()

    def get_all(self) -> List[TileDB]:
        stmt = select(TileDB)
        return self.session.execute(stmt).scalars().all()

    def delete_all(self) -> None:
        self.session.query(TileDB).delete()
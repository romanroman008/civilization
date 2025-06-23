from typing import List, Optional

from sqlalchemy.orm import Session

from db.models import Tile

class TileRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, tile: Tile) -> None:
        self.session.add(tile)

    def add_many(self, tiles: List[Tile]) -> None:
        self.session.add_all(tiles)

    def get_by_coordinates(self, x: int, y: int) -> Optional[Tile]:
        return self.session.query(Tile).filter_by(x=x, y=y).first()

    def get_all(self) -> List[Tile]:
        return self.session.query(Tile).all()

    def delete_all(self) -> None:
        self.session.query(Tile).delete()
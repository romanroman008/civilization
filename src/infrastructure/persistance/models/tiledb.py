from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistance.base import Base
from infrastructure.persistance.models.worlddb import WorldDB


class TileDB(Base):
    __tablename__ = 'tiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    x: Mapped[int] = mapped_column(index=True)
    y: Mapped[int] = mapped_column(index=True)
    terrain: Mapped[str] = mapped_column(String)


    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id"), nullable=False)
    world: Mapped["WorldDB"] = relationship(back_populates="tiles")

    def __repr__(self) -> str:
        return f"<Tile id={self.id} x={self.x} y={self.y} terrain='{self.terrain}'>"
from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistance.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infrastructure.persistance.models.tiledb import TileDB


class WorldDB(Base):
    __tablename__ = "worlds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    width: Mapped[int] = mapped_column(String, unique=True, nullable=False)
    height: Mapped[int] = mapped_column(String, unique=True, nullable=False)

    tiles: Mapped[List["TileDB"]] = relationship(
        back_populates="world",
        cascade="all, delete, delete-orphan"
    )
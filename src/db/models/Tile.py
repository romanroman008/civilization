from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Tile(Base):
    __tablename__ = 'tiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    x: Mapped[int] = mapped_column(index=True)
    y: Mapped[int] = mapped_column(index=True)
    terrain: Mapped[str] = mapped_column(String)

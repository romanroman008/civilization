from infrastructure.persistance.base import Base
from infrastructure.persistance.models.tiledb import TileDB

from infrastructure.persistance.repositories.tile_repository import TileRepository
from infrastructure.persistance.session import get_session, engine


def init_db():
    Base.metadata.create_all(bind=engine)

def ktos():
    tiles_to_add = [
        TileDB(x=0, y=0, terrain="grass"),
        TileDB(x=0, y=1, terrain="water"),
        TileDB(x=1, y=0, terrain="mountain"),
        TileDB(x=1, y=1, terrain="desert"),
    ]

    with get_session() as session:
        repo = TileRepository(session)
        repo.delete_all()
        repo.add(tiles_to_add[0])
        repo.add(tiles_to_add[0])
        repo.add_many(tiles_to_add)
        session.flush()
        print("Co w trawie piszczy:")
        all1= repo.get_all()
        for t in all1:
            print(f"jebaka siusiaka: {t}")


def cos():
    init_db()
    print("✅ Tabele zostały utworzone.")

    tiles_to_add = [
        TileDB(x=0, y=0, terrain="grass"),
        TileDB(x=0, y=1, terrain="water"),
        TileDB(x=1, y=0, terrain="mountain"),
        TileDB(x=1, y=1, terrain="desert"),
    ]

    with get_session() as session:
        print("👉 Dodawanie tile'ów do bazy...")
        session.add_all(tiles_to_add)
        session.flush()  # aby ID były widoczne jeszcze przed commitem
        for tile in tiles_to_add:
            print(f"✅ Dodano: {tile}")

    # Sprawdź co siedzi w bazie
    with get_session() as session:
        print("\n📦 Zawartość tabeli tiles:")
        all_tiles = session.query(TileDB).all()
        for tile in all_tiles:
            print(tile)
from infrastructure.Tile import Tile


class Chunk:
    def __init__(self, chunk_x: int, chunk_y: int, tiles: list[list[Tile]]):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.tiles = tiles
        self.loaded = True

    def get_tile(self, local_x: int, local_y: int) -> Tile:
        return self.tiles[local_y][local_x]

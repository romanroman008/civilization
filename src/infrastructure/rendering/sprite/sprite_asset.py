from infrastructure.rendering.sprite_loader import SpriteLoader


class SpriteAsset:
    def __init__(self,
                 name: str,
                 path: str,
                 tile_size: tuple[int, int],
                 anchor: tuple[int, int],
                 layer: int
                 ):
        self.name = name
        self.image = SpriteLoader.load(path)
        self.tile_size = tile_size
        self.anchor = anchor
        self.layer = layer
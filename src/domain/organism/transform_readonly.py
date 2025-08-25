class TransformReadOnly:
    __slots__ = ("x", "y", "rotation")
    def __init__(self, x: float = 0, y: float = 0, rotation: int = 0):
        self.x = x
        self.y = y
        self.rotation = rotation

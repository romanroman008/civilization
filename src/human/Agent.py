from Character import Character


class Agent:
    def __init__(self):
        self.health: float
        self.hunger: float
        self.energy: float
        self.age: int
        self.lifespan: int
        self.inventory: dict[str, int]
        self.inventory_limit: int
        self.vision_range: int
        self.character: Character








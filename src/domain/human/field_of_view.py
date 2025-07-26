from domain.components.position import Position
from domain.human.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.plant import Plant
from domain.world_map.world_perception import WorldPerception


class FieldOfView:
    def __init__(self, radius, world_perception: WorldPerception):
        self._radius = radius
        self._position = None
        self._world_perception = world_perception
        self._perceived_objects: list[PerceivedObject] = []

    def get_perceived_objects(self):
        positions = []
        for dx in range(-self._radius, self._radius + 1):
            for dy in range(-self._radius, self._radius + 1):
                positions.append(Position(dx, dy))

        return self._world_perception.get_visible_area(self._position, positions)


    def detect_edible_plants(self) -> list[PerceivedObject]:
        return [
            perc_obj for perc_obj in self._perceived_objects
            if (isinstance(perc_obj.organism, Plant)) and perc_obj.organism.is_edible
        ]

    def detect_animals(self):
        return [
            perc_obj for perc_obj in self._perceived_objects
            if (isinstance(perc_obj.organism, Animal))
        ]

    def detect_closest_animal(self):
        animals = self.detect_animals()
        if animals:
            return min(animals, key=lambda animal: animal.distance_to(self._position))
        return None


    def update(self, position: Position):
        self._position = position
        self._perceived_objects = self.get_perceived_objects()




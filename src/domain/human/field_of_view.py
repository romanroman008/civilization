from typing import Optional

from domain.components.position import Position
from domain.human.perception import animal_info
from domain.human.perception.animal_info import AnimalInfo
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
            if (isinstance(perc_obj.organism_info, Plant)) and perc_obj.organism_info.is_edible
        ]

    def detect_animals(self):
        return [
            perc_obj.organism_info for perc_obj in self._perceived_objects
            if (isinstance(perc_obj.organism_info, AnimalInfo))
        ]

    def detect_closest_animal(self) -> Optional[AnimalInfo]:
        animals = self.detect_animals()
        if not animals:
            return None

        return min(animals,
                   key=lambda animal: animal.relative_position.distance_to(self._position)
                   )





    def update(self, position: Position):
        self._position = position
        self._perceived_objects = self.get_perceived_objects()



    def _animal_to_animal_info(self, animal: Animal) -> AnimalInfo:
        relative_position = animal.position - self._position
        return AnimalInfo(animal.id, relative_position)
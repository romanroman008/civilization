from typing import Optional

from domain.components.position import Position

from domain.human.perception.animal_info import AnimalInfo
from domain.human.perception.organism_info import OrganismInfo
from domain.human.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.plant import Plant


from domain.world_map.world_facade import WorldFacade


class FieldOfView:
    def __init__(self, radius, world_facade: WorldFacade):
        self._radius = radius
        self._position = None
        self.world_facade = world_facade
        self._perceived_objects: list[PerceivedObject] = []
        self._organism_data: list[OrganismInfo] = []

    @property
    def perceived_objects(self):
        return self._perceived_objects

    def update_perceived_objects(self):
        positions = []
        x, y = self._position.x, self._position.y
        for dx in range(x - self._radius, x + self._radius + 1):
            for dy in range(y - self._radius, y + self._radius + 1):
                positions.append(Position(dx, dy))

        self._perceived_objects.clear()
        self._perceived_objects.extend(self.world_facade.get_visible_area(self._position, positions))


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
                   key=lambda animal: animal.relative_position.distance_to(Position(0,0))
                   )


    def update(self, position: Position):
        self._position = position
        self.update_perceived_objects()



    def _animal_to_animal_info(self, animal: Animal) -> AnimalInfo:
        relative_position = animal.position - self._position
        return AnimalInfo(animal.id, relative_position, animal.is_alive)
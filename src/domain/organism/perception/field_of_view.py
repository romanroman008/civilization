from typing import Optional

from domain.components.position import Position

from domain.organism.perception.animal_info import AnimalInfo
from domain.organism.perception.organism_info import OrganismInfo
from domain.organism.perception.percived_object import PerceivedObject
from domain.organism.instances.animal import Animal
from domain.organism.instances.plant import Plant
from domain.world_map.vision_port import VisionPort




class FieldOfView:
    def __init__(self, radius, vision_port: VisionPort):
        self._radius = radius
        self._position = None
        self._vision_port: VisionPort = vision_port
        self._perceived_objects: list[PerceivedObject] = []
        self._organism_data: list[OrganismInfo] = []
        self._target: Optional[OrganismInfo] = None



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
        self._perceived_objects.extend(self._vision_port.get_vision(self._position, positions))


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

    def detect_closest_animal(self, viewer: Animal) -> Optional[AnimalInfo]:
        animals = [a for a in self.detect_animals() if a.id != viewer.id and a.is_alive]
        if not animals:
            return None

        return min(
            animals,
            key=lambda animal: animal.relative_position.distance_to(Position(0, 0))
        )

    def update(self, position: Position):
        self._position = position
        self.update_perceived_objects()
        self._update_target()

    def _update_target(self):
        if self._target is None:
            return
        for perc_obj in self._perceived_objects:
            if perc_obj.organism_info is not None and perc_obj.organism_info.id == self._target.id:
                self._target.got_sighting(perc_obj.relative_position)
                if not perc_obj.organism_info.is_alive:
                    self._target.notify_its_death()

    def get_target_position(self, target: OrganismInfo) -> Optional[Position]:
        for po in self._perceived_objects:
            if po.organism_info is not None and po.organism_info.id == target.id:
                return po.organism_info.relative_position
        return None



    def _animal_to_animal_info(self, animal: Animal) -> AnimalInfo:
        relative_position = animal.position - self._position
        return AnimalInfo(animal.id, relative_position, animal.is_alive)
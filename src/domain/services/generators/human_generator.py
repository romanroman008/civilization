import random


from domain.components.position import Position
from domain.human.brain.brain import Brain
from domain.human.brain.human_brain import HumanBrain

from domain.human.field_of_view import FieldOfView
from domain.human.vitals import Vitals
from domain.organism.human_movement import HumanMovement

from domain.organism.instances.human import Human
from domain.organism.prefabs.organism_prefab import OrganismPrefab
from domain.services.event_bus import EventBus

from domain.world_map.world_facade import WorldFacade


from shared.config import CONFIG


def _get_random_positions(positions: list[Position], amount:int) -> list[Position]:
    return random.sample(positions, k=min(amount, len(positions)))

def create_vitals():
    return Vitals()

def create_field_of_view(radius: int, world_facade:WorldFacade) -> FieldOfView:
    return FieldOfView(radius, world_facade)

def create_movement() -> HumanMovement:
    return HumanMovement()

def create_brain(world_facade:WorldFacade, movement: HumanMovement, event_bus: EventBus) -> Brain:
    field_of_view = create_field_of_view(CONFIG["human_vision_radius"],world_facade)
    vitals = create_vitals()

    return HumanBrain(field_of_view, vitals, movement, event_bus)



class HumanGenerator:
    def __init__(self, count: int, species_distribution: list[tuple[OrganismPrefab, float]]):
        self.count = count
        self.species_distribution = species_distribution
        self.world_facade: WorldFacade | None = None


    def generate(self, world_facade: WorldFacade) -> WorldFacade:
        self.world_facade = world_facade
        event_bus = world_facade.event_bus


        for organism, fraction   in self.species_distribution:
            amount = int(fraction * self.count)
            available_positions = self._get_valid_positions(world_facade.height, world_facade.width, organism)
            approved_positions = _get_random_positions(available_positions, amount)
            animal_prefab = OrganismPrefab(organism.name, organism.allowed_terrains)

            for position in approved_positions:
                position = Position(3,3)
                movement = create_movement()
                brain = create_brain(world_facade, movement, event_bus)
                human = Human(animal_prefab, position, brain, movement)
                human.connect()
                world_facade.add_organism(human)


        return world_facade



    def _get_valid_positions(self, height: int, width: int, organism: OrganismPrefab) -> list[Position]:
        return [
            Position(x, y)
            for y in range (height)
            for x in range (width)
            if self.world_facade.is_position_allowed(Position(x,y), organism.allowed_terrains)
        ]









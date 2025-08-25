import logging
from collections import deque
from typing import Optional

from domain.components.direction import Direction
from domain.components.position import Position
from domain.components.terrain import Terrain
from domain.organism.brain.brain_interactions_handler import BrainInteractionsHandler
from domain.organism.perception.field_of_view import FieldOfView
from domain.organism.perception.animal_info import AnimalInfo

from domain.organism.perception.organism_info import OrganismInfo
from domain.organism.perception.percived_object import PerceivedObject
from domain.organism.vitals import Vitals
from domain.organism.instances.animal import Animal
from domain.organism.movement.movement import Movement

from domain.organism.state.hunting_state import HuntingState
from domain.organism.state.idle_state import IdleState
from domain.organism.state.walking_state import WalkingState

from domain.organism.strategy.random_walk_strategy import RandomWalkStrategy
from domain.services.event_bus import EventBus
from domain.services.movement.move_result import MoveResult
from shared.logger import get_logger





def _get_possible_move_neighbours(position: Position, perceived_objects: list[PerceivedObject]) -> dict[
    Direction, Position]:
    neighbours: dict[Direction, Position] = {}
    perceived_map = {
        obj.relative_position: obj
        for obj in perceived_objects
    }

    for direction in Direction:
        neighbour_pos = position + direction.vector()
        obj = perceived_map.get(neighbour_pos)
        if obj and obj.terrain == Terrain.GRASS:
            neighbours[direction] = neighbour_pos

    return neighbours


def find_shortest_path(goal: Position, perceived_objects: list[PerceivedObject]) -> Optional[list[Direction]]:
    queue = deque()
    start = Position(0, 0)
    queue.append((start, []))
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        for direction, neighbour_pos in _get_possible_move_neighbours(current, perceived_objects).items():
            if neighbour_pos in visited:
                continue
            visited.add(neighbour_pos)
            queue.append((neighbour_pos, path + [direction]))

    return None


class Brain:
    def __init__(self, field_of_view: FieldOfView, vitals: Vitals, movement: Movement, event_bus: EventBus):
        self._field_of_view = field_of_view
        self._vitals = vitals
        self._animal: Optional[Animal] = None
        self._movement = movement

        self._decision_strategy = RandomWalkStrategy()


        self._target: Optional[OrganismInfo] = None

        self._event_bus: EventBus = event_bus
        self._brain_interactions_handler: Optional[BrainInteractionsHandler]

        self._is_busy = False
        self._is_alive = True



        self._range = 1

    @property
    def is_alive(self) -> bool:
        return self._is_alive


    def _initialize_logger(self):
        self._logger = get_logger(f"Organism {self._animal.id}", level=logging.INFO, log_filename="organism.log")

    def _create_brain_interactions_handler(self):
        return BrainInteractionsHandler(organism=self._animal,
                                        brain=self,
                                        field_of_view=self._field_of_view,
                                        vitals=self._vitals,
                                        movement=self._movement,
                                        event_bus=self._event_bus)

    def tick(self):
        if not self._is_alive or self._is_busy:
            return
        self._is_busy = True



    def set_animal(self, animal: Animal):
        if self._animal is not None:
            raise RuntimeError("Animal already set")
        self._animal = animal
        self._brain_interactions_handler = self._create_brain_interactions_handler()
        self._field_of_view.update(self._animal.position)
        self._check_target_visibility()
        self._initialize_logger()

    async def update(self, payload):
        self._field_of_view.update(self._animal.position)
        self._check_target_visibility()


   

    async def walk(self, direction: Direction) -> MoveResult:
        result = await self._brain_interactions_handler.emit_walking_decision(direction)
        if result is MoveResult.SUCCESS:
            await self._animal.set_state(WalkingState())
            await self._movement.move_to(direction)
            await self._brain_interactions_handler.notify_position_change()
            await self._animal.set_state(IdleState())
        return result



    async def hunt(self):

        self._field_of_view.update(self._animal.position)
        closest_animal = self._field_of_view.detect_closest_animal(self._animal)
        if closest_animal is None:
            return []
        self._target = closest_animal
        path = self._plan_path_to_target()

        self._logger.info(f"walking sequence: {path}")
        await self._animal.set_state(HuntingState())
        i = 0
        while True:
            if self._is_target_in_range():
                await self._kill()
                break
            direction = path[0]
            i+=1

            result = await self.walk(direction)
            if result is MoveResult.SUCCESS:
                self._field_of_view.update(self._animal.position)
                self._update_target_position()
                self._logger.info(f"Iteracja {i}, pozycja targetu: {self._target.relative_position}")
                path = self._plan_path_to_target()
                if path is None:
                    self._logger.info(f"Path to target position: {self._target.relative_position} cannot be found from {self._animal.position}")


        await self._animal.set_state(IdleState())

    async def _kill(self):
       await self._brain_interactions_handler.emit_kill_decision(self._target.id)

    def _is_target_in_range(self):
        if self._target.relative_position.distance_to(Position(0,0)) <= self._range:
            return True
        return False


    def _update_target_position(self):
        updated_pos = self._field_of_view.get_target_position(self._target)
        if updated_pos is None:
            return
        self._target.got_sighting(updated_pos)




    def _plan_path_to_target(self) -> list[Direction]:
        destination = self._target.relative_position
        if isinstance(self._target, AnimalInfo):
            destination = (
                self._target.relative_position if self._target.is_visible
                else self._target.last_seen_position
            )
        return find_shortest_path(destination, self._field_of_view.perceived_objects)



    def kill_itself(self):
        self._is_alive = False



    def _check_target_visibility(self):
        if self._target is None:
            return

        match = next(
            (
                (perc_obj for perc_obj in self._field_of_view.perceived_objects()
                 if perc_obj.organism_info and perc_obj.organism_info.id == self._target.id)
            ),
            None
        )
        if match:
            self._target.got_sighting(match.organism_info.relative_position)
        else:
            self._target.lost_sighting()






import logging


from domain.components.terrain import Terrain
from domain.organism.brain.brain import Brain
from domain.organism.brain.path_planner import PathPlanner
from domain.organism.hunting.hunting import Hunting
from domain.organism.movement.action.action_status import ActionStatus
from domain.organism.movement.human_movement import HumanMovement
from domain.organism.organism_id import OrganismID
from domain.organism.perception.vision import Vision
from domain.organism.strategy.idle_strategy import IdleStrategy
from domain.organism.strategy.random_walk_strategy import RandomWalkStrategy

from domain.organism.transform.transform import TransformReadOnly

from domain.organism.vitals import Vitals



from domain.services.event_bus import EventBus
from shared.logger import get_logger


class HumanBrain(Brain):
    def __init__(self,
                 vision: Vision,
                 vitals: Vitals,
                 movement: HumanMovement,
                 path_planner: PathPlanner,
                 transform_readonly: TransformReadOnly,
                 allowed_terrains: set[Terrain],
                 event_bus: EventBus):
        super().__init__(vision, vitals, movement, path_planner, transform_readonly, allowed_terrains, event_bus)
        self._hunting = Hunting(movement, path_planner, vision, transform_readonly)



        self._decision_strategy = RandomWalkStrategy()

    def _initialize_logger(self):
        self._logger = get_logger(f"Human {self._owner_id}", level=logging.INFO, log_filename="human.log")

    def tick(self, tick: int):
        if not self._is_alive:
            return

        status = self._hunting.tick()
        if status == ActionStatus.RUNNING:
            self._status = status
            return

        status = self._movement.tick()
        if status == ActionStatus.SUCCESS:
            self._brain_interactions_handler.notify_position_change()
            status = ActionStatus.IDLE

        self._status = status

        if self._status is ActionStatus.IDLE and self._can_decide_this_tick(tick):
            self._vision.update()
            self.kill_animals_in_range()
            self._decision_strategy.decide(self)


    def hunt(self):
        self._hunting.hunt()

    def kill_animals_in_range(self):
        for animal_id in self._vision.get_animals_in_given_distance(self._range):
            self._brain_interactions_handler.emit_kill_decision(animal_id)


    def get_distance_to_target(self):
        x, y = self._transform_readonly.position.x, self._transform_readonly.position.y
        target_x, target_y = self._target.position
        offset_x, offset_y = self._target.offset
        target_x += offset_x / 100
        target_y += offset_y / 100
        return abs(target_x - x) + abs(target_y - y)



    def set_owner_id(self, organism_id: OrganismID):
        if self._owner_id:
            raise RuntimeError(f"Brain {organism_id} already has an owner")
        self._owner_id = organism_id
        self._brain_interactions_handler = self._create_brain_interactions_handler()
        self._phase = organism_id.id % self.DECIDE_BUCKETS
        self._initialize_logger()
        self._hunting.set_brain_interactions_handler(self._brain_interactions_handler)
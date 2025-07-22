import math

from domain.organism.organismdepr import OrganismDEPR
from domain.components.position import Position
from domain.services.movement.movement_system import find_needed_offset


class MovementInterpolation:
    rotation_speed = 1  # degrees per tick
    movement_speed = 10   # centimetre per tick

    def __init__(self, organisms: list[OrganismDEPR]):
        self._organisms = organisms

    def __call__(self, interval:float, *args, **kwargs):
        interval = 1000 * interval
        for organism in self._organisms:
            #with organism.lock:
            if organism.position == organism.target_position:
                continue


            if not self._is_facing_target(organism):
                self._rotate_organism(organism, interval)

            if self._is_facing_target(organism):
                self._move_organism(organism, interval)

            if self._has_reached_target(organism):
                self._finalize_movement(organism)

    def _rotate_organism(self, organism: OrganismDEPR, interval:float):
        rotation_step = int(math.copysign(10, organism.target_rotation))
        organism.rotate(rotation_step)

    def _move_organism(self, organism: OrganismDEPR, interval: float):
        desired_offset_x, desired_offset_y = find_needed_offset(organism)
        offset_x, offset_y = organism.offset

        if offset_x != desired_offset_x:
            offset_x_step =  0.1 * math.copysign(1, desired_offset_x)
            organism.move_offset_x(offset_x_step)

        if offset_y != desired_offset_y:
            offset_y_step = 0.1 * math.copysign(1, desired_offset_y)
            organism.move_offset_y(offset_y_step)

    def _is_facing_target(self, organism: OrganismDEPR) -> bool:
        return organism.facing == organism.target_facing


    def _has_reached_target(self, organism: OrganismDEPR) -> bool:
        offset_x, offset_y = organism.offset
        desired_offset_x, desired_offset_y = _find_needed_offset(organism)
        return (
            self._is_facing_target(organism)
            and offset_x == desired_offset_x
            and offset_y == desired_offset_y
        )

    def _finalize_movement(self, organism: OrganismDEPR):
        organism.position = Position(organism.target_position.x, organism.target_position.y)
        organism.reset_offset()
        #organism.reset_rotation()
        organism.isMoving = False



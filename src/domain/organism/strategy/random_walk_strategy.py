import random

from codetiming import Timer

from domain.components.direction import Direction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.organism.brain.brain import Brain
from domain.organism.strategy.decision_strategy import DecisionStrategy


class RandomWalkStrategy(DecisionStrategy):


    def decide(self, brain: "Brain"):
        directions = [d for delta in brain.get_possible_moves()
                      if (d := Direction.to_direction(delta)) is not None]

        if not directions:
            return
        direction = random.choice(directions)
        brain.walk(direction)

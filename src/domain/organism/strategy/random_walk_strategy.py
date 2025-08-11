import random

from domain.components.direction import Direction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.human.brain.brain import Brain
from domain.organism.strategy.decision_strategy import DecisionStrategy


class RandomWalkStrategy(DecisionStrategy):
    async def decide(self, brain: "Brain"):
        direction = random.choice(list(Direction))
        await brain.walk(direction)

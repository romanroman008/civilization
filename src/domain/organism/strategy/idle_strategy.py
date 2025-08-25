
from typing import TYPE_CHECKING

from domain.organism.strategy.decision_strategy import DecisionStrategy

if TYPE_CHECKING:
    from domain.organism.brain.brain import Brain


class IdleStrategy(DecisionStrategy):
    async def decide(self, brain: "Brain") -> None:
        pass

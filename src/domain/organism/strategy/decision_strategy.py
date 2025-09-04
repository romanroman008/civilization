from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.organism.brain.brain import Brain


class DecisionStrategy(ABC):
    @abstractmethod
    def decide(self, brain: "Brain") -> None:
        pass

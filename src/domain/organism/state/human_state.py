import logging
from abc import ABC, abstractmethod

from shared.logger import get_logger


class HumanState(ABC):
    logger = get_logger("HumanState", level=logging.INFO, log_filename="world.log")
    @abstractmethod
    async def on_enter(self, organism): pass
    async def on_exit(self, organism): pass
    async def on_tick(self, organism): pass


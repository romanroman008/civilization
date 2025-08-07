import logging
from abc import ABC, abstractmethod

from shared.logger import get_logger


class OrganismState(ABC):
    _logger = get_logger("Organism", level=logging.INFO, log_filename="world.log")
    def __init__(self):
        self._is_busy = False
    @abstractmethod
    async def on_enter(self, organism): pass
    async def on_exit(self, organism): pass
    @property
    def is_busy(self):
        return self._is_busy


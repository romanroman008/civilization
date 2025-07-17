import time
import threading
from typing import Callable

class GameClock:
    def __init__(self, logger, tick_interval: float = 1.0):
        self.logger = logger
        self.tick_interval = tick_interval
        self.tick_count = 0
        self._running = False
        self._thread = None
        self._subscribers: list[Callable[[int], None]] = []
        self._periodic_subscribers: list[tuple[int, Callable[[int], None]]] = []

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_loop)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def reset(self):
        self.tick_count = 0

    def subscribe(self, callback: Callable[[int], None]):
        self._subscribers.append(callback)

    def subscribe_every(self, n: int, callback: Callable[[int], None]):
        self._periodic_subscribers.append((n, callback))

    def _run_loop(self):
        while self._running:
            time.sleep(self.tick_interval)
            self.tick_count += 1
            self.logger.debug(f"Tick {self.tick_count}")

            for callback in self._subscribers:
                callback(self.tick_count)

            for interval, callback in self._periodic_subscribers:
                if self.tick_count % interval == 0:
                    callback(self.tick_count)

    def get_time(self) -> int:
        return self.tick_count

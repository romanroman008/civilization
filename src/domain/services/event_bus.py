import asyncio
from collections import defaultdict
from typing import Callable, Dict, Awaitable, Any


class EventBus:
    def __init__(self):
        self._listeners_sync: Dict[str, list[Callable[[dict], None]]] = defaultdict(list)
        self._command_handlers: Dict[str, Callable[[dict], Any]] = {}

    def on(self, event_type:str, callback:Callable[[dict], None]):
        self._listeners_sync[event_type].append(callback)

    def on_command(self, command_type: str, handler: Callable[[dict], Any]) -> None:
        if command_type in self._command_handlers:
            raise ValueError(f"Command handler for '{command_type}' already registered.")

        self._command_handlers[command_type] = handler

    def emit(self, event_type: str, payload: dict) -> None:
        for cb in list(self._listeners_sync.get(event_type, ())):  # kopia na wypadek modyfikacji listy
            try:
                cb(payload)
            except Exception as e:
                # zaloguj / zbierz błędy
                # print(f"Listener {cb} failed: {e}")
                pass



    def emit_with_response(self, command_type: str, payload: dict) -> Any:
        try:
            handler = self._command_handlers[command_type]
        except KeyError:
            raise ValueError(f"No command handler registered for '{command_type}'")

        return handler(payload)

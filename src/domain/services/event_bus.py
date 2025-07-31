import asyncio
from collections import defaultdict
from typing import Callable, Dict, Awaitable, Any


class EventBus:
    def __init__(self):
        self._listeners_sync: Dict[str, list[Callable[[dict], None]]] = defaultdict(list)
        self._listeners_async: Dict[str,list[Callable[[dict], Awaitable[None]]]] = defaultdict(list)
        self._command_handlers: Dict[str, Callable[[dict, asyncio.Future], Awaitable[None]]] = {}

    def on(self, event_type:str, callback:Callable[[dict], None]):
        self._listeners_sync[event_type].append(callback)

    def on_async(self, event_type:str, callback:Callable[[dict], Awaitable[None]]):
        self._listeners_async[event_type].append(callback)

    def on_command(self, event_type:str, callback:Callable[[dict, asyncio.Future], Awaitable[None]]):
        if event_type in self._command_handlers:
            raise ValueError(f"Command handler for '{event_type}' already registered.")
        self._command_handlers[event_type] = callback



    async def emit(self, event_type: str, payload: dict):
        listeners = self._listeners_sync.get(event_type, [])

        if not listeners:
            return

        await asyncio.gather(*(cb(payload) for cb in listeners))


    async def emit_with_response(self, event_type:str, payload: dict) -> Any:
        if event_type not in self._command_handlers:
            raise ValueError(f"No command handler registered for event '{event_type}'")

        future = asyncio.get_event_loop().create_future()

        handler = self._command_handlers[event_type]
        await handler(payload, future)

        return await future

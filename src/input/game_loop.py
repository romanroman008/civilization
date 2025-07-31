import asyncio
from typing import Optional

import pygame

from domain.components.direction import Direction
from domain.organism.human_movement import HumanMovement
from domain.organism.instances.human import Human
from domain.world_map.world_facade import WorldFacade
from domain.world_map.world_map import WorldMap
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.world_presenter import WorldPresenter
from infrastructure.rendering.world_renderer import WorldRenderer
from input.keyboard import Keyboard
from shared.config import CONFIG


def run_game(world_facade: WorldFacade, loop: asyncio.AbstractEventLoop):
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Civilization")

    tile_presenter = WorldPresenter()
    camera = Camera(0, 0,
                    CONFIG["screen_width"],
                    CONFIG["screen_height"],
                    CONFIG["map_width"],
                    CONFIG["map_height"],
                    CONFIG["tile_size"])
    world_renderer = WorldRenderer(screen,
                                   world_facade,
                                   tile_presenter,
                                   camera,
                                   tile_size=CONFIG["tile_size"])
    clock = pygame.time.Clock()
    running = True

    # 🔐 Flaga do blokowania inputu
    action_locked = False

    # 🧠 Agent kontrolowany przez gracza
    agent = get_agent(world_facade)

    async def handle_action(action: Optional[str]):
        nonlocal action_locked
        action_locked = True
        await decide(agent, action, loop)
        action_locked = False

    keyboard = Keyboard()

    while running:
        action = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keyboard.handle_event(event)

        dx, dy = keyboard.get_movement()
        camera.move(5 * dx, 5 * dy)

        action = keyboard.get_action()
        if action and not action_locked:
            action_locked = True
            safe_async(handle_action(action), loop)

        screen.fill((0, 0, 0))
        world_renderer.render_map(camera)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




async def decide(agent: Optional[Human], action: Optional[str], loop: asyncio.AbstractEventLoop):
    if agent is None:
        return
    if action is None:
        return


    action_map = {
        "stop": lambda: print("STOP"),
        "walk": lambda: agent.brain.walk(),
        "hunt": lambda: agent.brain.hunt()
    }

    func = action_map.get(action)
    if func:
        await func()
    else:
        print(f"[WARN] Unknown action: {action}")



def get_agent(world_facade: WorldFacade) -> Optional[Human]:
    agent = world_facade.get_example_agent()
    return agent

def safe_async(coro, loop: asyncio.AbstractEventLoop):
    try:
        asyncio.run_coroutine_threadsafe(coro, loop)
    except Exception as e:
        print(f"[ERROR] Failed to schedule async action: {e}")



import asyncio
from typing import Optional

import pygame

from domain.components.direction import Direction
from domain.organism.human_movement import HumanMovement
from domain.organism.instances.human import Human
from domain.world_map.world_map import WorldMap
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.world_presenter import WorldPresenter
from infrastructure.rendering.world_renderer import WorldRenderer
from input.keyboard import Keyboard
from shared.config import CONFIG


def run_game(world: WorldMap, loop: asyncio.AbstractEventLoop):
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Civilization")

    tile_presenter = WorldPresenter(world)

    camera = Camera(0,0,
                    CONFIG["screen_width"],
                    CONFIG["screen_height"],
                    CONFIG["map_width"],
                    CONFIG["map_height"],
                    CONFIG["tile_size"])
    world_renderer = WorldRenderer(screen,
                                   world,
                                   tile_presenter,
                                   camera,
                                   tile_size=CONFIG["tile_size"])

    clock = pygame.time.Clock()
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keyboard = Keyboard()
        dx, dy = keyboard.get_movement()
        action = keyboard.get_action()
        camera.move(5*dx,5*dy)
        if action:
            asyncio.run_coroutine_threadsafe(
                decide(get_agent(world), action, loop),
                loop
            )



        screen.fill((0, 0, 0))
        world_renderer.render_map(camera)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

async def decide(agent: Optional[Human], action: Optional[str], loop: asyncio.AbstractEventLoop):
    if agent is None or action is None:
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



def get_agent(world: WorldMap) -> Optional[Human]:
    for organism in world.organisms:
        if isinstance(organism, Human):
            return organism
    return None

def safe_async(coro, loop: asyncio.AbstractEventLoop):
    try:
        asyncio.run_coroutine_threadsafe(coro, loop)
    except Exception as e:
        print(f"[ERROR] Failed to schedule async action: {e}")



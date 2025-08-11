import asyncio
from typing import Optional

import pygame
from asyncio import Queue

from domain.components.direction import Direction
from domain.organism.instances.animal import Animal
from domain.organism.instances.human import Human
from domain.world_map.world_facade import WorldFacade
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.world_presenter import WorldPresenter
from infrastructure.rendering.world_renderer import WorldRenderer
from input.keyboard import Keyboard
from shared.config import CONFIG


async def render_loop(world_renderer: WorldRenderer, camera: Camera, screen):
    while True:
        screen.fill((0, 0, 0))
        world_renderer.render_map(camera)
        pygame.display.flip()
        await asyncio.sleep(1 / 60)  # ~60 FPS

async def game_loop(agent: Human, action_queue: Queue):
    action_locked = False

    async def handle_action(action: Optional[str]):
        nonlocal action_locked
        action_locked = True
        await decide(agent, action)
        action_locked = False

    while True:
        action = await action_queue.get()
        if not action_locked:
            await handle_action(action)




from asyncio import Queue

async def input_loop(keyboard: Keyboard, camera: Camera, action_queue: Queue):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            keyboard.handle_event(event)

        dx, dy = keyboard.get_movement()
        if dx != 0 or dy != 0:
            camera.move(5 * dx, 5 * dy)

        action = keyboard.get_action()
        if action:
            await action_queue.put(action)

        await asyncio.sleep(1 / 60)

async def organism_loop(world_facade: WorldFacade):
    while True:
        await world_facade.tick()
        await asyncio.sleep(1)


async def run_game(world_facade: WorldFacade):
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
    agent = get_agent(world_facade)
    keyboard = Keyboard()

    action_queue = asyncio.Queue()

    await asyncio.gather(
        asyncio.create_task(render_loop(world_renderer, camera, screen)),
        asyncio.create_task(game_loop(agent, action_queue)),
        asyncio.create_task(input_loop(keyboard, camera, action_queue)),
        asyncio.create_task(organism_loop(world_facade)),

    )



    pygame.quit()



async def decide(agent: Optional[Animal], action: Optional[str]):
    if agent is None or action is None:
        return

    action_map = {
        "stop": lambda: print("STOP"),
        "walk": lambda: agent._brain.walk(Direction.TOP),
        "hunt": lambda: agent._brain.hunt(),
        "up": lambda: agent._brain.walk(Direction.TOP),
        "down": lambda: agent._brain.walk(Direction.BOT),
        "left": lambda: agent._brain.walk(Direction.LEFT),
        "right": lambda: agent._brain.walk(Direction.RIGHT),
    }


    func = action_map.get(action)
    if func:
        await func()
    else:
        print(f"[WARN] Unknown action: {action}")


def get_agent(world_facade: WorldFacade) -> Optional[Human]:
    return world_facade.get_example_agent()

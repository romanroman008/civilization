import pygame

from domain.world.services.world_service import WorldService
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.world_presenter import WorldPresenter
from infrastructure.rendering.world_renderer import WorldRenderer
from interface import keyboard
from interface.keyboard import Keyboard
from shared.config import CONFIG


def run_game(world):
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Civilization")

    tile_presenter = WorldPresenter(world)

    camera = Camera(0,0,CONFIG["screen_width"],CONFIG["screen_height"], CONFIG["map_height"], CONFIG["map_height"])
    world_renderer = WorldRenderer(screen,world,tile_presenter)

    clock = pygame.time.Clock()
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keyboard = Keyboard()
        dx, dy = keyboard.get_movement()
        camera.move(5*dx,5*dy)



        screen.fill((0, 0, 0))
        world_renderer.render_map(camera)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
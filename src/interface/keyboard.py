import pygame
from shared.config import DEFAULT_KEY_BINDINGS

# Mapa nazw klawiszy (z configa) na kody Pygame
NAME_TO_PYGAME_KEY = {
    "w": pygame.K_w,
    "a": pygame.K_a,
    "s": pygame.K_s,
    "d": pygame.K_d,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
}

class Keyboard:
    def __init__(self, bindings: dict[str, str] = DEFAULT_KEY_BINDINGS):
        self.key_bindings = {
            NAME_TO_PYGAME_KEY[bindings["move_up"]]: (0, -1),
            NAME_TO_PYGAME_KEY[bindings["move_down"]]: (0, 1),
            NAME_TO_PYGAME_KEY[bindings["move_left"]]: (-1, 0),
            NAME_TO_PYGAME_KEY[bindings["move_right"]]: (1, 0),
        }

    def get_movement(self) -> tuple[int, int]:
        """Zwraca kierunek ruchu jako (dx, dy)."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        for key, (x, y) in self.key_bindings.items():
            if keys[key]:
                dx += x
                dy += y
        return dx, dy

import pygame
import os

class SpriteLoader:
    _cache: dict[str, pygame.Surface] = {}

    @classmethod
    def load(cls, path: str) -> pygame.Surface:
        if path not in cls._cache:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            full_path = os.path.join(base_path, path)

            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Sprite not found: {full_path}")

            image = pygame.image.load(full_path)


            if pygame.display.get_init():
                image = image.convert_alpha()

            cls._cache[path] = image

        return cls._cache[path]

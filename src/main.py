from application.services.world_setup import create_elevation_noise_generator, create_elevation_generator, \
    create_world_generator

from interface.game_loop import run_game
from shared.config import CONFIG
from shared.logger import get_logger

from view.presentation.preview import show_layer

from view.presentation.layers.layer_factory import create_terrain_layer


def main():
    logger = get_logger("civilization")

    elevation_noise_generator = create_elevation_noise_generator(CONFIG)
    elevation_generator = create_elevation_generator(elevation_noise_generator, CONFIG)
    world_generator = create_world_generator(logger, elevation_generator)

    world = world_generator.generate_map(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])

    show_layer(create_terrain_layer(world))

    run_game(world)


if __name__ == "__main__":
    main()

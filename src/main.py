from application.services.world_setup import create_elevation_noise_generator, create_elevation_generator, \
    create_world_generator
from domain.world.entieties.organism.plant import Plant
from domain.world.entieties.terrain import Terrain
from domain.world.services.generators.plants_generator import PlantsGenerator

from domain.world.services.generators.world_generator import WorldGenerator
from domain.world.services.world_service import WorldService
from infrastructure.persistance.base import Base
from infrastructure.persistance.session import engine

from interface.game_loop import run_game
from shared.config import CONFIG
from shared.logger import get_logger





species_dist = [
    (Plant(name="Berries", allowed_terrains={Terrain.GRASS}), 1),
    (Plant(name="Tree", allowed_terrains={Terrain.GRASS}, block_radius=1), 1)
]


count = 400


def create_world_service(world_generator:WorldGenerator):
    return WorldService(world_generator)


def init_db():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def main():
    logger = get_logger("civilization")

    elevation_noise_generator = create_elevation_noise_generator(CONFIG)
    elevation_generator = create_elevation_generator(elevation_noise_generator, CONFIG)

    plants_generator = PlantsGenerator(count, species_dist)

    world_generator = create_world_generator(logger, elevation_generator, plants_generator)


    init_db()


    world_service = create_world_service(world_generator)

    world = None
    world = world_service.create_new_world(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])

    # try:
    #     world = world_service.get_world_by_name("Rr4")
    #     logger.info(f"World {world.name} already exists")
    # except ValueError:
    #     world = world_service.create_new_world(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])
    #     world.name = "Rr4"
    #     world_service.save_world(world)
    #     logger.info(f"World {world.name} created")
    #
    # # show_layer(create_terrain_layer(world))

    run_game(world)



if __name__ == "__main__":

    main()

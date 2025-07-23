import logging

from bootstrap.world_setup import create_world_generator, create_world_service, create_movement_system

from infrastructure.persistance.base import Base
from infrastructure.persistance.session import engine

from input.game_loop import run_game
from shared.config import CONFIG
from shared.logger import get_logger

from apscheduler.schedulers.background import BackgroundScheduler


def init_db():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)



def main():
    logger = get_logger("civilization")
    scheduler = BackgroundScheduler()
    aps_logger = logging.getLogger("apscheduler")
    aps_logger.setLevel(logging.CRITICAL)  # wyciszenie lub WARNING
    aps_logger.propagate = False
    aps_logger.handlers = logger.handlers[:]  # ← Twoje własne handlery

    world_generator = create_world_generator(logger)

    init_db()

    world_service = create_world_service(world_generator)

    world = None
    world = world_service.create_new_world(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])

    movement_system = create_movement_system(logger, world)



    scheduler.start()
    scheduler.add_job(lambda: movement_system(2), 'interval', seconds=2)

    for o in world.organisms:
        scheduler.add_job(o, 'interval', seconds=0.01)


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
    scheduler.shutdown()


if __name__ == "__main__":
    main()

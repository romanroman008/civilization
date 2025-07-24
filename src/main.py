import logging

from apscheduler.events import EVENT_JOB_MISSED

from bootstrap.world_setup import create_world_generator, create_world_service, create_movement_system
from domain.organism.orchestrator import Orchestrator

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
    # aps_logger = logging.getLogger("apscheduler")
    # aps_logger.propagate = False
    # aps_logger.handlers = logger.handlers[:]  # ← Twoje własne handlery



    world_generator = create_world_generator(logger)

    init_db()

    world_service = create_world_service(world_generator)

    world = None
    world = world_service.create_new_world(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])

    movement_system = create_movement_system(logger, world)
    scheduler.remove_all_jobs()

    def listener(event):
        print("MISSED job:", event.job_id)

    scheduler.add_listener(listener, EVENT_JOB_MISSED)

    scheduler.start()
    scheduler.add_job(lambda: movement_system(5), 'interval', seconds=2)

    orchestrator = Orchestrator(world.organisms)

    scheduler.add_job(orchestrator,'interval', seconds=0.01, max_instances=5)



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
    scheduler.shutdown(wait=True)


if __name__ == "__main__":
    main()

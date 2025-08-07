import asyncio




from bootstrap.world_setup import create_world_generator, create_world_service


from infrastructure.persistance.base import Base
from infrastructure.persistance.session import engine

from input.game_loop import run_game
from shared.config import CONFIG
from shared.logger import get_logger




def init_db():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)



def main():
    logger = get_logger("civilization")
    # aps_logger = logging.getLogger("apscheduler")
    # aps_logger.propagate = False
    # aps_logger.handlers = logger.handlers[:]  # ← Twoje własne handlery



    world_generator = create_world_generator(logger)

    init_db()

    world_service = create_world_service(world_generator)

    world = None
    #world = world_service.create_new_world(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])

    world_facade = world_generator.create(CONFIG["map_width"], CONFIG["map_height"], CONFIG["scale"])









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

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    import threading
    threading.Thread(target=loop.run_forever, daemon=True).start()

    asyncio.run(run_game(world_facade))





if __name__ == "__main__":
    main()

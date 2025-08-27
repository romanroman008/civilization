import pygame

from domain.components.direction import Direction
from domain.world_map.world_facade import WorldFacade
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.soa.world_frame_snapshot import WorldFrameSnapshot

from infrastructure.rendering.world_renderer import WorldRenderer
from infrastructure.rendering.world_snapshot_adapter import WorldSnapshotAdapter
from input.keyboard import Keyboard
from shared.config import CONFIG



def run_game(world_facade: WorldFacade, world_snapshot_adapter: WorldSnapshotAdapter):
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Civilization")

    camera = Camera(offset_x=0, offset_y=0, screen_width=CONFIG["screen_width"],screen_height=CONFIG["screen_height"],
                    map_width= CONFIG["map_width"], map_height= CONFIG["map_height"], tile_size=CONFIG["tile_size"])

    renderer = WorldRenderer(screen, camera, tile_size=CONFIG["tile_size"])
    keyboard = Keyboard()
    agent = world_facade.get_example_agent()

    game = Game(world_facade,world_snapshot_adapter, renderer, camera, keyboard, agent)
    game.run()
    pygame.quit()



class Game:
    def __init__(self, world: WorldFacade, world_snapshot_adapter: WorldSnapshotAdapter, renderer: WorldRenderer, camera, keyboard, agent):
        self.world_facade = world
        self.world_snapshot_adapter = world_snapshot_adapter
        self.renderer = renderer
        self.camera = camera
        self.keyboard = keyboard
        self.agent = agent
        self.running = True

        self.prev_snap: WorldFrameSnapshot = world_snapshot_adapter.make_snapshot()
        self.curr_snap: WorldFrameSnapshot = self.prev_snap
        self.clock = pygame.time.Clock()

    # --- Fazy pętli: małe, czytelne metody ---

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.keyboard.handle_event(event)

    def update_camera(self) -> None:
        dx, dy = self.keyboard.get_movement()
        if dx or dy:
            self.camera.move(dx,dy)

    def process_actions(self) -> None:
        action = self.keyboard.get_action()
        if not action or not self.agent:
            return
        # bez await — szybkie akcje; dłuższe rzeczy batchujemy w ticku
        action_map = {
            "stop": lambda: None,
            "walk": lambda: self.agent._brain.walk(Direction.TOP),
            "hunt": lambda: self.agent._brain.hunt(),
            "up":   lambda: self.agent._brain.walk(Direction.TOP),
            "down": lambda: self.agent._brain.walk(Direction.BOT),
            "left": lambda: self.agent._brain.walk(Direction.LEFT),
            "right":lambda: self.agent._brain.walk(Direction.RIGHT),
        }
        func = action_map.get(action)
        if func:
            func()

    def step_fixed_logic(self) -> None:
        """Jeden deterministyczny krok logiki + przygotowanie snapshotu."""
        self.prev_snap = self.curr_snap
        self.world_facade.tick()
        self.curr_snap = self.world_snapshot_adapter.make_snapshot()



    def render_frame(self) -> None:
        self.renderer.surface.fill((0, 0, 0))
        self.renderer.render_map(self.curr_snap)
        pygame.display.flip()


    # --- Pętla główna ---

    def run(self) -> None:
        while self.running:
            self.process_events()
            self.update_camera()
            self.process_actions()
            self.step_fixed_logic()
            self.render_frame()

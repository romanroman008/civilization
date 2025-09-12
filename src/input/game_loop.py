import pygame

from codetiming import Timer
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

    world_snapshot_adapter.set_camera(camera)

    game = Game(world_facade,world_snapshot_adapter, renderer, camera, keyboard, agent)
    game.run()
    pygame.quit()

RENDER_HZ = 60
LOGIC_HZ = 60

class Game:
    def __init__(self, world: WorldFacade, world_snapshot_adapter: WorldSnapshotAdapter, renderer: WorldRenderer, camera, keyboard, agent):
        self.world_facade = world
        self.world_snapshot_adapter = world_snapshot_adapter
        self.renderer = renderer
        self.camera = camera
        self.keyboard = keyboard
        self.agent = agent
        self.running = True



        self.curr_snap = world_snapshot_adapter.make_snapshot(True)

        self.clock = pygame.time.Clock()

        self.LOGIC_EVENT = pygame.event.custom_type()
        self.RENDER_EVENT = pygame.event.custom_type()

        pygame.time.set_timer(self.LOGIC_EVENT, int(1000 / LOGIC_HZ))
        pygame.time.set_timer(self.RENDER_EVENT, int(1000 / RENDER_HZ))

        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP,
                                  self.LOGIC_EVENT, self.RENDER_EVENT])

        self.max_logic_ticks_per_frame = 8
        self.remaining_ticks_amount = 0


    # --- Fazy pętli: małe, czytelne metody ---

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.keyboard.handle_event(event)

    def update_camera(self) -> bool:
        dx, dy = self.keyboard.get_movement()
        if dx or dy:
            self.camera.move(dx,dy)
            return True
        return False

    @Timer(name="logic", text="logic: {milliseconds:.1f}ms")
    def step_fixed_logic(self, steps: int = 1) -> None:
        max_ticks = self.max_logic_ticks_per_frame
        if steps > max_ticks:
            self.remaining_ticks_amount += steps - max_ticks
            steps = max_ticks
        for _ in range(steps):
            self.world_facade.tick()

    @Timer(name="snapshot", text="snapshot: {milliseconds:.1f}ms")
    def build_snapshot(self):
        self.curr_snap = self.world_snapshot_adapter.make_snapshot(False)

    @Timer(name="render", text="render: {milliseconds:.1f}ms")
    def render_frame(self) -> None:
     #   self.renderer.surface.fill((0, 0, 0))
        self.renderer.render_map(self.curr_snap)
        pygame.display.flip()

    # --- Pętla główna ---

    def run(self) -> None:
        self.curr_snap = self.world_snapshot_adapter.make_snapshot(True)
        self.render_frame()
        while self.running:

            event = pygame.event.wait()

            logic_ticks = self.remaining_ticks_amount
            render_request = False

            # obsłuż pierwsze zdarzenie
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.LOGIC_EVENT:
                logic_ticks += 1
            elif event.type == self.RENDER_EVENT:
                render_request = True
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.keyboard.handle_event(event)

            if not self.running:
                break


            if logic_ticks:
                self.step_fixed_logic(logic_ticks)

            if render_request:
                self.update_camera()
                self.build_snapshot()
                self.render_frame()


            # if event.type == pygame.QUIT:
            #     self.running = False
            # if event.type == self.LOGIC_EVENT:
            #     self.step_fixed_logic()
            # if event.type == self.RENDER_EVENT:
            #     camera_moved = self.update_camera()
            #     snapshot = self.world_snapshot_adapter.make_snapshot(camera_moved)
            #     self.render_frame(snapshot)



            # self.process_events()
            # self.update_camera()
            #
            # self.step_fixed_logic()
            # self.render_frame()

            # if event.type == self.RENDER_EVENT:
            #     camera = self.update_camera()
            #     self.render_frame(self.world_snapshot_adapter.make_snapshot(True))
            #
            # if event.type == self.LOGIC_EVENT:
            #     self.step_fixed_logic()



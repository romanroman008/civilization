import pygame

from codetiming import Timer

from domain.components.direction import Direction
from domain.world_map.world_facade import WorldFacade
from infrastructure.rendering.camera import Camera
from infrastructure.rendering.soa.world_frame_snapshot import WorldFrameSnapshot

from infrastructure.rendering.world_renderer import WorldRenderer
from infrastructure.rendering.world_snapshot_adapter import WorldSnapshotAdapter
from input.keyboard import Keyboard
from shared.config import CONFIG
from view.gui import AppUI
from view.pause_result import PauseResult



def run_game(world_facade: WorldFacade, world_snapshot_adapter: WorldSnapshotAdapter):
    pygame.init()
    screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
    pygame.display.set_caption("Civilization")

    camera = Camera(offset_x=0, offset_y=0,
                    screen_width=CONFIG["screen_width"], screen_height=CONFIG["screen_height"],
                    map_width=CONFIG["map_width"], map_height=CONFIG["map_height"], tile_size=CONFIG["tile_size"])

    renderer = WorldRenderer(screen, camera, tile_size=CONFIG["tile_size"])
    keyboard = Keyboard()
    agent = world_facade.get_example_agent()

    world_snapshot_adapter.set_camera(camera)

    ui = AppUI()
    game = Game(world_facade, world_snapshot_adapter, renderer, camera, keyboard, agent, screen, ui_service=ui)
    game.run()
    pygame.quit()


RENDER_HZ = 60
LOGIC_HZ = 120

class Game:
    def __init__(self,
                 world: WorldFacade,
                 world_snapshot_adapter: WorldSnapshotAdapter,
                 renderer: WorldRenderer,
                 camera, keyboard, agent,
                 screen,
                 ui_service):
        self.world_facade = world
        self.world_snapshot_adapter = world_snapshot_adapter
        self.renderer = renderer
        self.camera = camera
        self.keyboard = keyboard
        self.agent = agent
        self.running = True
        self._ui = ui_service

        self.screen = screen
        self._paused = False



        self.curr_snap = world_snapshot_adapter.make_snapshot(True)

        self.clock = pygame.time.Clock()

        self.LOGIC_EVENT = pygame.event.custom_type()
        self.RENDER_EVENT = pygame.event.custom_type()

        pygame.time.set_timer(self.LOGIC_EVENT, int(1000 / LOGIC_HZ))
        pygame.time.set_timer(self.RENDER_EVENT, int(1000 / RENDER_HZ))

        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
                                  self.LOGIC_EVENT, self.RENDER_EVENT])

        self.max_logic_ticks_per_frame = 8
        self.remaining_ticks_amount = 0

        self.tick_id = 0


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

    #@Timer(name="logic", text="logic: {milliseconds:.1f}ms")
    def step_fixed_logic(self, steps: int = 1) -> None:
        """Wykonuje co najwyżej max_logic_ticks_per_frame kroków logiki.
        Nadwyżkę dopisuje do remaining_ticks_amount, a tick_id przesuwa o realnie wykonane kroki."""
        max_ticks = self.max_logic_ticks_per_frame
        if steps > max_ticks:
            self.remaining_ticks_amount += steps - max_ticks
            steps = max_ticks

        tick_start = self.tick_id
        for i in range(steps):
            self.world_facade.tick(tick_start + i)

        # PRZESUŃ globalny licznik ticków o faktycznie zrobione kroki
        self.tick_id = tick_start + steps

    def build_snapshot(self):
        self.curr_snap = self.world_snapshot_adapter.make_snapshot(False)


    def render_frame(self) -> None:
     #   self.renderer.surface.fill((0, 0, 0))
        self.renderer.render_map(self.curr_snap)
        pygame.display.flip()

    def proccess_action(self):
        action = self.keyboard.get_action()
        if action == "hunt":
            self.agent._brain.hunt()
        elif action == "up":
            self.agent._brain.walk(Direction.TOP)
        elif action == "down":
            self.agent._brain.walk(Direction.BOT)
        elif action == "left":
            self.agent._brain.walk(Direction.LEFT)
        elif action == "right":
            self.agent._brain.walk(Direction.RIGHT)
        elif action == "pause":
            result = self._ui.show_pause_overlay(self.screen)  # <- Pygame overlay NA TYM EKRANIE
            if result is PauseResult.MAIN_MENU:
                self.running = False
                setattr(self, "_back_to_menu", True)  # opcjonalnie sygnał dla wyższej warstwy
            else:
                # po powrocie z pauzy wyczyść zaległe ticki z timerów, żeby nie "nadrabiać"
                pygame.event.clear([self.LOGIC_EVENT, self.RENDER_EVENT])

    def run(self) -> None:
        # początkowy render
        self.curr_snap = self.world_snapshot_adapter.make_snapshot(True)
        self.render_frame()

        while self.running:
            # Zacznij od ewentualnie zaległych ticków z poprzedniej iteracji
            logic_ticks = self.remaining_ticks_amount
            self.remaining_ticks_amount = 0  # ZERUJ – wszystko od teraz policzymy na nowo
            render_request = False
            action_request = False

            # Czekaj na pierwsze zdarzenie by nie kręcić się “na sucho”
            first_event = pygame.event.wait()
            events = [first_event] + pygame.event.get()  # DRain kolejki

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == self.LOGIC_EVENT:
                    self.tick_id += 1
                    logic_ticks += 1
                elif event.type == self.RENDER_EVENT:
                    render_request = True
                elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    # adapter zwraca True/False jeśli jest “action”
                    action_request = self.keyboard.handle_event(event) or action_request

            if not self.running:
                break

            if action_request:
                self.proccess_action()  # wykona 0..n akcji (w tym pauzę)

            if logic_ticks:
                self.step_fixed_logic(logic_ticks)

            if render_request:
                self.update_camera()
                self.build_snapshot()
                self.render_frame()






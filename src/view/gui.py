# plik: view/app_ui.py
import tkinter as tk
from tkinter import ttk
from enum import Enum, auto
from typing import Optional
import pygame

import main
from view.pause_result import PauseResult

# ======= style (menu główne – Tk) =======
PALETTE = {
    "bg":          "#0f141a",
    "fg":          "#e6e6e6",
    "primary":     "#3a86ff",
    "primary_hov": "#5aa0ff",
    "danger":      "#ef4444",
    "danger_hov":  "#f06262",
}
FONT_BASE  = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 14, "bold")


class MainMenuChoice(Enum):
    START = auto()
    EXIT  = auto()


class AppUI:
    """Warstwa UI:
    - menu główne (Tkinter),
    - pauza jako overlay w oknie gry (Pygame).
    """

    # === MENU GŁÓWNE (Tkinter) ===
    def show_main_menu(self) -> MainMenuChoice:
        root = tk.Tk()
        root.title("Civilization – Menu")
        self._center(root, 360, 220)
        self._apply_style()

        container = ttk.Frame(root, padding=16, style="App.TFrame")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="Civilization", style="Title.TLabel").pack(pady=(0, 12))

        decision: Optional[MainMenuChoice] = None
        def choose(val: MainMenuChoice):
            nonlocal decision
            decision = val
            root.destroy()

        ttk.Button(container, text="Start",  width=24, style="Primary.TButton",
                   command=lambda: choose(MainMenuChoice.START)).pack(pady=(0, 10))
        ttk.Button(container, text="Wyjście", width=24, style="Danger.TButton",
                   command=lambda: choose(MainMenuChoice.EXIT)).pack()

        root.bind("<Return>", lambda e: choose(MainMenuChoice.START))
        root.bind("<Escape>", lambda e: choose(MainMenuChoice.EXIT))

        root.mainloop()
        return decision or MainMenuChoice.EXIT

    # === PAUZA (Pygame overlay na tym samym ekranie) ===
    def show_pause_overlay(self, screen: pygame.Surface) -> PauseResult:
        """
        Półprzezroczysta pauza z dwoma przyciskami:
        - Wznów [ESC]
        - Do menu
        Renderowana NA TYM SAMYM ekranie gry (brak drugiego okna).
        Zwraca PauseResult.RESUME lub PauseResult.MAIN_MENU.
        """
        clock = pygame.time.Clock()
        w, h = screen.get_size()

        # Nakładka i czcionki
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        title_font = pygame.font.SysFont(None, 56)
        btn_font   = pygame.font.SysFont(None, 28)
        hint_font  = pygame.font.SysFont(None, 22)

        # Geometria przycisków
        btn_w, btn_h, gap = 260, 48, 12
        cx, cy = w // 2, h // 2 + 16
        resume_rect = pygame.Rect(0, 0, btn_w, btn_h); resume_rect.center = (cx, cy)
        menu_rect   = pygame.Rect(0, 0, btn_w, btn_h); menu_rect.center   = (cx, cy + btn_h + gap)

        # Kolory
        BTN, BTN_HOV   = (58, 134, 255), (90, 160, 255)
        BTN2, BTN2_H   = (75, 85, 99),   (98, 108, 123)
        WHITE, MUTED   = (255, 255, 255), (220, 220, 220)

        def draw_button(rect: pygame.Rect, label: str, base, hover) -> bool:
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, hover if hovered else base, rect, border_radius=8)
            text = btn_font.render(label, True, WHITE)
            screen.blit(text, text.get_rect(center=rect.center))
            return hovered

        paused = True
        while paused:
            clicked = False

            # Pobieramy tylko zdarzenia ważne dla pauzy, by nie mieszać kolejki
            for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]):
                if event.type == pygame.QUIT:
                    return PauseResult.MAIN_MENU
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return PauseResult.RESUME
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True

            # Rysowanie na AKTUALNYM kadrze gry
            screen.blit(overlay, (0, 0))
            title = title_font.render("PAUZA", True, WHITE)
            screen.blit(title, title.get_rect(center=(w // 2, h // 2 - 48)))

            hovered_resume = draw_button(resume_rect, "Wznów  [ESC]", BTN,  BTN_HOV)
            hovered_menu   = draw_button(menu_rect,   "Do menu",      BTN2, BTN2_H)

            hint = hint_font.render("Kliknij przycisk lub naciśnij ESC", True, MUTED)
            screen.blit(hint, hint.get_rect(center=(w // 2, menu_rect.bottom + 24)))

            if clicked and hovered_resume:
                return PauseResult.RESUME
            if clicked and hovered_menu:
                return PauseResult.MAIN_MENU

            pygame.display.flip()
            clock.tick(30)

    # ==== helpers (Tk styl i centrowanie) ====
    def _apply_style(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except: pass
        style.configure(".", font=FONT_BASE)
        style.configure("App.TFrame", background=PALETTE["bg"])
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["fg"])
        style.configure("Title.TLabel", background=PALETTE["bg"],
                        foreground=PALETTE["fg"], font=FONT_TITLE)
        style.configure("TButton", padding=10)
        style.configure("Primary.TButton", padding=10, foreground="white",
                        background=PALETTE["primary"], borderwidth=0)
        style.map("Primary.TButton", background=[("active", PALETTE["primary_hov"])])
        style.configure("Danger.TButton", padding=10, foreground="white",
                        background=PALETTE["danger"], borderwidth=0)
        style.map("Danger.TButton", background=[("active", PALETTE["danger_hov"])])

    def _center(self, root: tk.Tk, w: int, h: int):
        root.update_idletasks()
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.configure(bg=PALETTE["bg"])




def run_app():
    ui = AppUI()
    while True:
        choice = ui.show_main_menu()
        if choice is MainMenuChoice.EXIT:
            break
        main.create_game()



if __name__ == "__main__":
    run_app()

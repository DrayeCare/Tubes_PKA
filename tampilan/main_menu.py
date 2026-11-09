"""
tampilan/main_menu.py
Main Menu (PLACEHOLDER, FULLSCREEN): hanya tampilan, belum terhubung ke layar lain.
File ini berdiri sendiri (tidak mengimpor ui.py) supaya tidak ada import melingkar.

Tombol: 1. Mulai   2. Setting   3. Info   4. Quit
Keluar: tombol Quit, angka 4, atau ESC.

show_main_menu(screen) -> "mulai" | "setting" | "info" | "quit"

Tes mandiri: py -3.13 -m tampilan.main_menu
"""

import pygame
from core import config

MENU_SIZE = (680, 560)  # ukuran acuan desain; layout diskalakan ke layar penuh
FPS = getattr(config, "FPS", 60)

COLOR_BG = getattr(config, "COLOR_BG", (0, 0, 0))
COLOR_PACMAN = getattr(config, "COLOR_PACMAN", (255, 220, 0))
C_MENU_BG = (8, 8, 20)
C_TITLE = (110, 220, 255)
C_SUBTITLE = (190, 190, 190)
C_TEXT = (235, 235, 245)
C_MUTED = (140, 140, 170)
C_LINE = (60, 60, 100)
C_BTN = (40, 40, 70)
C_BTN_HOVER = (62, 62, 110)

MENU_ITEMS = [
    ("mulai", "1. Mulai"),
    ("setting", "2. Setting"),
    ("info", "3. Info"),
    ("quit", "4. Quit"),
]

_fonts = {}


def _font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("consolas", size, bold=bold)
    return _fonts[key]


def _text(screen, msg, size, color, center, bold=False):
    surf = _font(size, bold).render(str(msg), True, color)
    screen.blit(surf, surf.get_rect(center=center))


class Button:
    def __init__(self, rect, label, value, font_size=22):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.font_size = font_size

    def draw(self, screen):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, C_BTN_HOVER if hover else C_BTN, self.rect, border_radius=10)
        pygame.draw.rect(screen, C_LINE, self.rect, 2, border_radius=10)
        _text(screen, self.label, self.font_size, C_TEXT, self.rect.center)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))


def show_main_menu(screen=None):
    # Layar penuh sesuai resolusi monitor
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pac-Man AI: BFS vs A*")
    w, h = screen.get_size()
    clock = pygame.time.Clock()

    # Skala layout terhadap tinggi layar (acuan 560 px)
    s = h / MENU_SIZE[1]
    btn_w, btn_h, gap = int(320 * s), int(60 * s), int(20 * s)
    total_h = 4 * btn_h + 3 * gap
    top = int(h * 0.36)
    top = min(top, h - total_h - int(30 * s))  # jaga agar tombol tidak keluar layar
    buttons = [
        Button((w // 2 - btn_w // 2, top + i * (btn_h + gap), btn_w, btn_h),
               label, value, font_size=int(24 * s))
        for i, (value, label) in enumerate(MENU_ITEMS)
    ]
    keymap = {pygame.K_1: "mulai", pygame.K_2: "setting",
              pygame.K_3: "info", pygame.K_4: "quit"}

    title_size, sub_size = int(64 * s), int(20 * s)
    title_y, sub_y = int(h * 0.14), int(h * 0.14) + int(58 * s)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key in keymap:
                    return keymap[event.key]
            for b in buttons:
                if b.clicked(event):
                    return b.value

        screen.fill(C_MENU_BG)
        _text(screen, "GHOST vs PAC-MAN", title_size, C_TITLE, (w // 2, title_y), bold=True)
        _text(screen, "BFS  |  A*  -  AI Search Comparison", sub_size, C_SUBTITLE,
              (w // 2, sub_y), bold=True)
        for b in buttons:
            b.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # Placeholder: hanya cetak pilihan, belum membuka layar apa pun.
    print("Pilihan:", show_main_menu(scr))
    pygame.quit()
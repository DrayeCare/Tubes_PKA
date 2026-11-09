import json
import os

import pygame
from core import config

FPS = getattr(config, "FPS", 60)

SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "settings.json"
)
CONTROL_CHOICES = ("wasd", "arrow")
DEFAULT_CONTROLS = "wasd"


def _read_saved():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            value = json.load(f).get("controls")
    except (OSError, ValueError, AttributeError):
        return None
    return value if value in CONTROL_CHOICES else None


def load_controls():
    return _read_saved() or DEFAULT_CONTROLS


def save_controls(value):
    if value not in CONTROL_CHOICES:
        return False
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump({"controls": value}, f)
    except OSError:
        return False
    return True


def get_movement_keys(controls=None):
    controls = controls or load_controls()
    if controls == "arrow":
        return {"up": [pygame.K_UP], "down": [pygame.K_DOWN],
                "left": [pygame.K_LEFT], "right": [pygame.K_RIGHT]}
    return {"up": [pygame.K_w], "down": [pygame.K_s],
            "left": [pygame.K_a], "right": [pygame.K_d]}

C_BG = (8, 8, 20)
C_TITLE = (110, 220, 255)
C_SUBTITLE = (190, 190, 190)
C_LABEL = (200, 200, 200)
C_TEXT = (235, 235, 245)
C_SUBTEXT = (210, 210, 226)
C_MUTED = (154, 154, 184)
C_BORDER = (240, 240, 250)
C_CARD = (30, 30, 48)
C_CARD_ACTIVE = (85, 60, 130)
C_CARD_ACTIVE_BORDER = (195, 150, 255)
C_KEY = (42, 42, 62)
C_KEY_BORDER = (140, 140, 170)
C_KEY_SHADOW = (20, 20, 31)
C_BACK = (70, 45, 100)
C_SAVE = (40, 125, 60)
C_MENU = (42, 42, 62)
C_OK = (80, 220, 120)
C_ERR = (255, 100, 100)
C_CHECK_DARK = (26, 16, 48)

_fonts = {}
def _font(size, bold=False):
    key = (max(int(size), 8), bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("consolas", key[0], bold=bold)
    return _fonts[key]


def _text(screen, msg, size, color, center, bold=False):
    surf = _font(size, bold).render(str(msg), True, color)
    screen.blit(surf, surf.get_rect(center=center))


def _lighten(color, amount=18):
    return tuple(min(255, v + amount) for v in color)


def _draw_arrow(screen, rect, direction, color, s):
    dx, dy = direction
    px, py = -dy, dx
    cx, cy = rect.center
    L = 9 * s
    width = max(int(3 * s), 2)
    tip = (cx + dx * L, cy + dy * L)
    tail = (cx - dx * L, cy - dy * L)
    base = (tip[0] - dx * L * 0.8, tip[1] - dy * L * 0.8)
    wing1 = (base[0] + px * L * 0.8, base[1] + py * L * 0.8)
    wing2 = (base[0] - px * L * 0.8, base[1] - py * L * 0.8)
    pygame.draw.line(screen, color, tail, tip, width)
    pygame.draw.line(screen, color, wing1, tip, width)
    pygame.draw.line(screen, color, wing2, tip, width)


def _draw_keycap(screen, rect, s, label=None, arrow=None):
    shadow = rect.move(0, int(4 * s))
    pygame.draw.rect(screen, C_KEY_SHADOW, shadow, border_radius=8)
    pygame.draw.rect(screen, C_KEY, rect, border_radius=8)
    pygame.draw.rect(screen, C_KEY_BORDER, rect, 2, border_radius=8)
    if label:
        _text(screen, label, int(26 * s), C_TEXT, rect.center, bold=True)
    if arrow:
        _draw_arrow(screen, rect, arrow, C_TEXT, s)


def _draw_check(screen, center, s):
    cx, cy = center
    pygame.draw.circle(screen, C_CARD_ACTIVE_BORDER, center, int(16 * s))
    pts = [(cx - 7 * s, cy + 0.5 * s), (cx - 2 * s, cy + 5 * s), (cx + 7 * s, cy - 5 * s)]
    pygame.draw.lines(screen, C_CHECK_DARK, False, pts, max(int(3 * s), 2))

class Button:
    def __init__(self, rect, label, value, font_size, fill, bold=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.font_size = font_size
        self.fill = fill
        self.bold = bold

    def draw(self, screen):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = _lighten(self.fill) if hover else self.fill
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, C_BORDER, self.rect, 2, border_radius=10)
        _text(screen, self.label, self.font_size, C_TEXT, self.rect.center, self.bold)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))


class ControlCard:
    KEY_SIZE, KEY_GAP = 60, 8

    def __init__(self, rect, value, title, subtitle):
        self.rect = pygame.Rect(rect)
        self.value = value
        self.title = title
        self.subtitle = subtitle

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))

    def draw(self, screen, active, s):
        if active:
            fill, border, bw = C_CARD_ACTIVE, C_CARD_ACTIVE_BORDER, 4
        else:
            fill, border, bw = C_CARD, C_BORDER, 2
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            fill = _lighten(fill)
        pygame.draw.rect(screen, fill, self.rect, border_radius=14)
        pygame.draw.rect(screen, border, self.rect, bw, border_radius=14)

        k, g = int(self.KEY_SIZE * s), int(self.KEY_GAP * s)
        grid_w = 3 * k + 2 * g
        gx = self.rect.centerx - grid_w // 2
        gy = self.rect.top + int(24 * s)

        def cell(col, row):
            return pygame.Rect(gx + col * (k + g), gy + row * (k + g), k, k)

        if self.value == "wasd":
            _draw_keycap(screen, cell(1, 0), s, label="W")
            _draw_keycap(screen, cell(0, 1), s, label="A")
            _draw_keycap(screen, cell(1, 1), s, label="S")
            _draw_keycap(screen, cell(2, 1), s, label="D")
        else:
            _draw_keycap(screen, cell(1, 0), s, arrow=(0, -1))
            _draw_keycap(screen, cell(0, 1), s, arrow=(-1, 0))
            _draw_keycap(screen, cell(1, 1), s, arrow=(0, 1))
            _draw_keycap(screen, cell(2, 1), s, arrow=(1, 0))

        _text(screen, self.title, int(30 * s), C_TEXT,
              (self.rect.centerx, self.rect.top + int(192 * s)), bold=True)
        _text(screen, self.subtitle, int(15 * s), C_SUBTEXT,
              (self.rect.centerx, self.rect.top + int(234 * s)))

        if active:
            _draw_check(screen, (self.rect.right - int(30 * s), self.rect.top + int(30 * s)), s)

def show_setting(screen=None):
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pac-Man AI: BFS vs A*")
    w, h = screen.get_size()
    clock = pygame.time.Clock()
    s = h / 720
    cx = w // 2

    saved_choice = _read_saved()
    selected = saved_choice or DEFAULT_CONTROLS
    save_failed = False

    back_rect = pygame.Rect(int(24 * s), int(24 * s), int(72 * s), int(52 * s))

    card_w, card_h, card_gap = int(380 * s), int(280 * s), int(40 * s)
    card_top = int(214 * s)
    cards = [
        ControlCard((cx - card_gap // 2 - card_w, card_top, card_w, card_h),
                    "wasd", "WASD", "W atas | A kiri | S bawah | D kanan"),
        ControlCard((cx + card_gap // 2, card_top, card_w, card_h),
                    "arrow", "PANAH", "Panah atas | kiri | bawah | kanan"),
    ]

    btn_w, btn_h, btn_gap = int(260 * s), int(60 * s), int(30 * s)
    btn_top = int(530 * s)
    save_btn = Button((cx - btn_gap // 2 - btn_w, btn_top, btn_w, btn_h),
                      "SIMPAN", "save", int(24 * s), C_SAVE)
    menu_btn = Button((cx + btn_gap // 2, btn_top, btn_w, btn_h),
                      "KE MENU", "menu", int(22 * s), C_MENU)

    def do_save():
        nonlocal saved_choice, save_failed
        if save_controls(selected):
            saved_choice = selected
            save_failed = False
        else:
            save_failed = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    do_save()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return "menu"
            for card in cards:
                if card.clicked(event):
                    selected = card.value
                    save_failed = False
            if save_btn.clicked(event):
                do_save()
            if menu_btn.clicked(event):
                return "menu"
        screen.fill(C_BG)

        hover = back_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, _lighten(C_BACK) if hover else C_BACK, back_rect,
                         border_radius=10)
        pygame.draw.rect(screen, C_BORDER, back_rect, 2, border_radius=10)
        _draw_arrow(screen, back_rect, (-1, 0), (255, 255, 255), s * 1.1)

        _text(screen, "SETTING", int(48 * s), C_TITLE, (cx, int(72 * s)), bold=True)
        _text(screen, "GHOST vs PAC-MAN", int(18 * s), C_SUBTITLE, (cx, int(116 * s)),
              bold=True)
        _text(screen, "KONTROL PAC-MAN", int(22 * s), C_LABEL, (cx, int(181 * s)), bold=True)

        for card in cards:
            card.draw(screen, active=(selected == card.value), s=s)

        save_btn.draw(screen)
        menu_btn.draw(screen)

        if save_failed:
            _text(screen, "Gagal menyimpan pengaturan", int(17 * s), C_ERR,
                  (cx, int(620 * s)), bold=True)
        elif saved_choice == selected:
            _text(screen, "Pengaturan tersimpan", int(17 * s), C_OK,
                  (cx, int(620 * s)), bold=True)
        else:
            _text(screen, "Belum disimpan", int(17 * s), C_MUTED,
                  (cx, int(620 * s)), bold=True)

        _text(screen, "Klik kartu untuk memilih | ENTER = simpan | "
                      "ESC atau panah kiri atas = kembali ke menu utama",
              int(14 * s), C_MUTED, (cx, int(692 * s)))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    print("Hasil:", show_setting(scr), "| kontrol tersimpan:", load_controls())
    pygame.quit()
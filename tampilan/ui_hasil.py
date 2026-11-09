"""
tampilan/ui_hasil.py
Layar Hasil (FULLSCREEN): ditampilkan saat game selesai.

Isi layar:
    - Judul: BERHASIL KABUR! (Pac-Man menang) / TERTANGKAP! (Ghost menang)
    - Keterangan singkat + info maze dan algoritma Ghost
    - Tiga kartu: Waktu Pencarian, Jumlah Simpul yang Diperiksa, Panjang Jalur
    - Tombol MAIN LAGI (Enter) dan KE MENU (ESC)

show_hasil(screen, winner, stats, info=None) -> "replay" | "menu" | "quit"

    winner : "pacman" atau "ghost"
    stats  : {"search_time_ms": 0.342,   # waktu pencarian dalam milidetik
              "nodes_explored": 87,      # jumlah simpul yang diperiksa
              "path_length": 15}         # panjang jalur (langkah)
             Semua key opsional; yang tidak ada ditampilkan "-".
             Mau rata-rata atau total, itu ditentukan oleh yang mengisi stats
             (game.py / recorder.py).
    info   : {"maze": 1|2|3, "algorithm": "bfs"|"astar"}   (opsional)

Contoh di game.py:
    from tampilan.ui_hasil import show_hasil
    aksi = show_hasil(screen, "pacman",
                      {"search_time_ms": avg_ms, "nodes_explored": total_nodes,
                       "path_length": len(path)},
                      {"maze": 2, "algorithm": "astar"})

Tes mandiri:
    py -3.13 -m tampilan.ui_hasil          (Pac-Man menang)
    py -3.13 -m tampilan.ui_hasil ghost    (Ghost menang)
"""

import math
import sys

import pygame

from core import config

FPS = getattr(config, "FPS", 60)

# ---------------------------------------------------------------------------
# Warna
# ---------------------------------------------------------------------------
C_BG = (8, 8, 20)
C_WIN = (80, 220, 120)
C_LOSE = (255, 100, 100)
C_REASON = (210, 210, 226)
C_INFO = (154, 154, 184)
C_LABEL = (200, 200, 200)
C_VALUE = (110, 220, 255)
C_UNIT = (190, 190, 190)
C_TEXT = (235, 235, 245)
C_CARD = (30, 30, 48)
C_BORDER = (240, 240, 250)
C_ICON_BG = (42, 42, 62)
C_ICON_BORDER = (140, 140, 170)
C_BTN_PLAY = (40, 125, 60)
C_BTN_MENU = (42, 42, 62)
C_HINT = (154, 154, 184)

MAZE_NAMES = {1: "Mudah", 2: "Sedang", 3: "Sulit"}
ALGO_NAMES = {"bfs": "BFS", "astar": "A*"}

# ---------------------------------------------------------------------------
# Format teks (fungsi murni, mudah dites)
# ---------------------------------------------------------------------------


def _fmt_time(value):
    return "-" if value is None else f"{float(value):.3f}"


def _fmt_int(value):
    return "-" if value is None else str(int(value))


def _info_line(info):
    """Contoh: 'Maze Sedang | Algoritma Ghost: A*'. Bagian yang tidak ada dilewati."""
    info = info or {}
    parts = []
    if info.get("maze") in MAZE_NAMES:
        parts.append(f"Maze {MAZE_NAMES[info['maze']]}")
    if info.get("algorithm") in ALGO_NAMES:
        parts.append(f"Algoritma Ghost: {ALGO_NAMES[info['algorithm']]}")
    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Helper gambar
# ---------------------------------------------------------------------------
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


def _arc(cx, cy, r, start_deg, end_deg, steps=10):
    """Titik-titik busur lingkaran (sumbu y ke bawah)."""
    return [
        (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        for a in [
            start_deg + (end_deg - start_deg) * i / steps for i in range(steps + 1)
        ]
    ]


def _draw_icon(screen, kind, center, s):
    """Ikon 34px (skala viewBox 24) di tengah lingkaran ikon."""
    k = 34 / 24 * s
    ox, oy = center
    width = max(int(2 * k), 2)

    def p(x, y):  # koordinat viewBox (pusat 12,12) -> layar
        return (ox + (x - 12) * k, oy + (y - 12) * k)

    if kind == "time":
        pygame.draw.circle(screen, C_VALUE, center, int(9 * k), width)
        pygame.draw.lines(
            screen, C_VALUE, False, [p(12, 7), p(12, 12), p(15, 14)], width
        )
    elif kind == "nodes":
        for x, y in ((6, 6), (18, 6), (12, 18)):
            pygame.draw.circle(screen, C_VALUE, p(x, y), int(2.5 * k), width)
        pygame.draw.line(screen, C_VALUE, p(8.5, 6), p(15.5, 6), width)
        pygame.draw.line(screen, C_VALUE, p(7.2, 8.2), p(10.8, 15.8), width)
        pygame.draw.line(screen, C_VALUE, p(16.8, 8.2), p(13.2, 15.8), width)
    else:  # "path"
        pygame.draw.circle(screen, C_VALUE, p(5, 18), int(2.2 * k), width)
        pygame.draw.circle(screen, C_VALUE, p(19, 6), int(2.2 * k), width)
        pts = [p(7.2, 18), p(13, 18)]
        pts += [
            p(x, y) for x, y in _arc(13, 15, 3, 90, -90)
        ]  # busur kanan (turun ke naik)
        pts += [p(11, 12)]
        pts += [p(x, y) for x, y in _arc(11, 9, 3, 90, 270)]  # busur kiri
        pts += [p(16.8, 6)]
        pygame.draw.lines(screen, C_VALUE, False, pts, width)


class Button:
    def __init__(self, rect, label, value, font_size, fill):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.font_size = font_size
        self.fill = fill

    def draw(self, screen):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = _lighten(self.fill) if hover else self.fill
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, C_BORDER, self.rect, 2, border_radius=10)
        _text(screen, self.label, self.font_size, C_TEXT, self.rect.center, bold=True)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class StatCard:
    def __init__(self, rect, icon, label, value, unit):
        self.rect = pygame.Rect(rect)
        self.icon = icon
        self.label = label
        self.value = value
        self.unit = unit

    def draw(self, screen, s):
        cx = self.rect.centerx
        top = self.rect.top
        pygame.draw.rect(screen, C_CARD, self.rect, border_radius=14)
        pygame.draw.rect(screen, C_BORDER, self.rect, 2, border_radius=14)

        icon_center = (cx, top + int(56 * s))
        pygame.draw.circle(screen, C_ICON_BG, icon_center, int(32 * s))
        pygame.draw.circle(screen, C_ICON_BORDER, icon_center, int(32 * s), 2)
        _draw_icon(screen, self.icon, icon_center, s)

        _text(
            screen,
            self.label,
            int(16 * s),
            C_LABEL,
            (cx, top + int(110 * s)),
            bold=True,
        )
        _text(
            screen,
            self.value,
            int(54 * s),
            C_VALUE,
            (cx, top + int(160 * s)),
            bold=True,
        )
        _text(
            screen, self.unit, int(20 * s), C_UNIT, (cx, top + int(210 * s)), bold=True
        )


# ---------------------------------------------------------------------------
# Layar Hasil
# ---------------------------------------------------------------------------
def show_hasil(screen=None, winner="pacman", stats=None, info=None):
    if screen is None:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pac-Man AI: BFS vs A*")
    w, h = screen.get_size()
    clock = pygame.time.Clock()
    s = min(h / 720, w / 1280)  # skala layout (acuan 1280 x 720)
    cx = w // 2

    stats = stats or {}
    ghost_win = winner == "ghost"
    title = "TERTANGKAP!" if ghost_win else "BERHASIL KABUR!"
    title_color = C_LOSE if ghost_win else C_WIN
    reason = (
        "Ghost berhasil menangkap Pac-Man"
        if ghost_win
        else "Pac-Man sampai di Exit, Ghost gagal mengejar"
    )
    info_line = _info_line(info)

    # --- tiga kartu ---
    card_w, card_h, gap = int(360 * s), int(260 * s), int(28 * s)
    total_w = 3 * card_w + 2 * gap
    x0 = cx - total_w // 2
    card_top = int(228 * s)
    specs = [
        ("time", "WAKTU PENCARIAN", _fmt_time(stats.get("search_time_ms")), "ms"),
        (
            "nodes",
            "JUMLAH SIMPUL YANG DIPERIKSA",
            _fmt_int(stats.get("nodes_explored")),
            "simpul",
        ),
        ("path", "PANJANG JALUR", _fmt_int(stats.get("path_length")), "langkah"),
    ]
    cards = [
        StatCard((x0 + i * (card_w + gap), card_top, card_w, card_h), *spec)
        for i, spec in enumerate(specs)
    ]

    # --- tombol ---
    btn_w, btn_h, btn_gap = int(260 * s), int(60 * s), int(30 * s)
    btn_top = card_top + card_h + int(48 * s)
    play_btn = Button(
        (cx - btn_gap // 2 - btn_w, btn_top, btn_w, btn_h),
        "MAIN LAGI",
        "replay",
        int(24 * s),
        C_BTN_PLAY,
    )
    menu_btn = Button(
        (cx + btn_gap // 2, btn_top, btn_w, btn_h),
        "KE MENU",
        "menu",
        int(22 * s),
        C_BTN_MENU,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "replay"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            if play_btn.clicked(event):
                return "replay"
            if menu_btn.clicked(event):
                return "menu"

        # --- gambar ---
        screen.fill(C_BG)
        _text(screen, title, int(60 * s), title_color, (cx, int(86 * s)), bold=True)
        _text(screen, reason, int(20 * s), C_REASON, (cx, int(142 * s)), bold=True)
        if info_line:
            _text(screen, info_line, int(17 * s), C_INFO, (cx, int(176 * s)), bold=True)

        for card in cards:
            card.draw(screen, s)

        play_btn.draw(screen)
        menu_btn.draw(screen)

        _text(
            screen,
            "ENTER = main lagi | ESC = ke menu utama",
            int(14 * s),
            C_HINT,
            (cx, h - int(30 * s)),
        )

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pemenang = "ghost" if "ghost" in sys.argv else "pacman"
    aksi = show_hasil(
        scr,
        pemenang,
        {"search_time_ms": 0.342, "nodes_explored": 87, "path_length": 15},
        {"maze": 2, "algorithm": "astar"},
    )
    print("Aksi:", aksi)
    pygame.quit()

import pygame

from core import config

FPS = getattr(config, "FPS", 60)
C_BG = (8, 8, 20)
C_TITLE = (255, 255, 255)
C_LABEL = (200, 200, 200)
C_ENEMY_LABEL = (255, 140, 140)
C_TEXT = (235, 235, 245)
C_CARD = (30, 30, 48)
C_BTN = (42, 42, 62)
C_BORDER = (240, 240, 250)

C_MAZE_ACTIVE_FILL = (85, 60, 130)
C_MAZE_ACTIVE_BORDER = (195, 150, 255)
C_ENEMY_ACTIVE_FILL = (110, 40, 50)
C_ENEMY_ACTIVE_BORDER = (255, 100, 100)
C_BACK_FILL = (70, 45, 100)
C_START_FILL = (40, 125, 60)

C_WALL = (34, 34, 221)
C_PATH = (0, 0, 0)
C_EXIT = (0, 200, 0)
C_PACMAN = (255, 220, 0)
C_GHOST = (255, 0, 0)


MAP_OPTIONS = [
    (1, "Maze Mudah - Banyak Jalur Alternatif"),
    (2, "Maze Sedang - Loop dan Percabangan"),
    (3, "Maze Sulit - Loop Bersarang dan Belokan"),
]

ALGO_OPTIONS = [("bfs", "BFS"), ("astar", "A*")]

MAP_PREVIEWS = {
    1: {
        "grid": [
            "#####################",
            "#...................#",
            "#.#####.#####.#.###.#",
            "#.....#..#....#.....#",
            "#.###...#####.#.###.#",
            "#.#...#...........#.#",
            "#.#.###.##.##.###.#.#",
            "#...#...............#",
            "##.##.###.#.###.###.#",
            "#.......#...#.......#",
            "#.##.##.#.#.#.##.##.#",
            "#...................#",
            "##.##.###.#.###.###.#",
            "#...............#...#",
            "#.#.###.##.##.#.#.#.#",
            "#.#...#.......#...#.#",
            "#.###.#.#####.#.###.#",
            "#.............#.....#",
            "#.#####.#####.#.###.#",
            "#...................#",
            "#####################",
        ],
        "exit": (1, 4),
        "ghost": (13, 17),
        "pacman": (19, 3),
    },
    2: {
        "grid": [
            "#####################",
            "#.......#...........#",
            "#.#####.#.#####.###.#",
            "#.....#...#.........#",
            "#.###.##.##.#.####.##",
            "#...#.......#.......#",
            "###.#.###.###.#####.#",
            "#.....#...........#.#",
            "#.###.#.#######.#.#.#",
            "#.....#.......#.#...#",
            "#.###...#####...###.#",
            "#.....#.......#.#...#",
            "#.###.#.###.###.#.#.#",
            "#.....#.#.........#.#",
            "#####.#.##.##.###.#.#",
            "#...........#.......#",
            "#.###.###.#.#.#.###.#",
            "#.....#...#...#.....#",
            "#.#####.#.#.###.###.#",
            "#.......#...........#",
            "#####################",
        ],
        "exit": (1, 11),
        "ghost": (12, 15),
        "pacman": (19, 14),
    },
    3: {
        "grid": [
            "#####################",
            "#...#...............#",
            "#.#.#.#####.#.#####.#",
            "#.#...#.....#.....#.#",
            "#.#####.#########...#",
            "#.....#...........#.#",
            "#####...######.####.#",
            "#.....#.....#.......#",
            "#.###.#.###.#.#####.#",
            "#.....#...#...#.....#",
            "#.###.######.##.#.###",
            "#.....#...#...#.....#",
            "#.###.#.###.#.#.###.#",
            "#...........#.......#",
            "#####.#.###.###.###.#",
            "#.....#.#.........#.#",
            "#.###.#.#.#######.#.#",
            "#.#.........#.....#.#",
            "#.#.#.#####...###.#.#",
            "#...#.......#.......#",
            "#####################",
        ],
        "exit": (3, 4),
        "ghost": (9, 17),
        "pacman": (19, 18),
    },
}
_fonts = {}


def _font(size, bold=False):
    key = (max(int(size), 8), bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("consolas", key[0], bold=bold)
    return _fonts[key]


def _text(screen, msg, size, color, center, bold=False):
    surf = _font(size, bold).render(str(msg), True, color)
    screen.blit(surf, surf.get_rect(center=center))


def _fit_size(msg, max_w, start, bold=False):
    """Ukuran font terbesar (<= start) agar teks muat dalam max_w."""
    size = int(start)
    while size > 8 and _font(size, bold).size(msg)[0] > max_w:
        size -= 1
    return size


def _lighten(color, amount=18):
    return tuple(min(255, v + amount) for v in color)


def _build_preview(data, side):
    """Gambar labirin menjadi Surface (tanpa jalur), maksimal side x side."""
    rows = data["grid"]
    n, m = len(rows), len(rows[0])
    cell = max(side // max(n, m), 2)
    surf = pygame.Surface((cell * m, cell * n))
    surf.fill(C_PATH)
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch == "#":
                pygame.draw.rect(surf, C_WALL, (c * cell, r * cell, cell, cell))
    pad = max(cell // 5, 1)
    er, ec = data["exit"]
    pygame.draw.rect(
        surf, C_EXIT, (ec * cell + pad, er * cell + pad, cell - 2 * pad, cell - 2 * pad)
    )
    for key, color in (("pacman", C_PACMAN), ("ghost", C_GHOST)):
        r, c = data[key]
        pygame.draw.circle(
            surf,
            color,
            (c * cell + cell // 2, r * cell + cell // 2),
            max(cell // 2 - 1, 2),
        )
    return surf


class Button:
    def __init__(self, rect, label, value=None, font_size=20, bold=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.font_size = font_size
        self.bold = bold

    def hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, fill=C_BTN, border=C_BORDER, border_w=2, text_color=C_TEXT):
        color = _lighten(fill) if self.hovered() else fill
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, border, self.rect, border_w, border_radius=10)
        _text(
            screen, self.label, self.font_size, text_color, self.rect.center, self.bold
        )

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class MapCard:
    def __init__(self, rect, maze_id, caption, preview, caption_size, pad):
        self.rect = pygame.Rect(rect)
        self.maze_id = maze_id
        self.caption = caption
        self.preview = preview
        self.caption_size = caption_size
        self.pad = pad

    def hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, active):
        if active:
            fill, border, bw = C_MAZE_ACTIVE_FILL, C_MAZE_ACTIVE_BORDER, 4
        else:
            fill, border, bw = C_CARD, C_BORDER, 2
        if self.hovered():
            fill = _lighten(fill)
        pygame.draw.rect(screen, fill, self.rect, border_radius=12)
        pygame.draw.rect(screen, border, self.rect, bw, border_radius=12)

        pr = self.preview.get_rect(midtop=(self.rect.centerx, self.rect.top + self.pad))
        screen.blit(self.preview, pr)
        _text(
            screen,
            self.caption,
            self.caption_size,
            C_TEXT,
            (self.rect.centerx, (pr.bottom + self.rect.bottom) // 2),
            bold=True,
        )

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def show_mulai(screen=None):
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Pac-Man AI: BFS vs A*")
    w, h = screen.get_size()
    clock = pygame.time.Clock()
    s = h / 760

    sel = {"maze": 1, "algorithm": "bfs"}
    back_btn = Button(
        (int(16 * s), int(16 * s), int(120 * s), int(46 * s)),
        "BACK",
        "back",
        int(20 * s),
        bold=True,
    )

    pad = int(12 * s)
    gap = int(24 * s)
    card_w = min(int(w * 0.29), int(380 * s))
    side = min(card_w - 2 * pad, int(h * 0.33))
    caption_h = int(h * 0.08)
    card_h = pad + side + caption_h
    total_w = 3 * card_w + 2 * gap
    x0 = (w - total_w) // 2
    card_top = int(h * 0.19)

    caption_size = min(
        _fit_size(cap, card_w - 2 * pad, 20 * s, bold=True) for _, cap in MAP_OPTIONS
    )
    cards = []
    for i, (maze_id, caption) in enumerate(MAP_OPTIONS):
        rect = (x0 + i * (card_w + gap), card_top, card_w, card_h)
        preview = _build_preview(MAP_PREVIEWS[maze_id], side)
        cards.append(MapCard(rect, maze_id, caption, preview, caption_size, pad))

    algo_w, algo_h, algo_gap = int(220 * s), int(56 * s), int(30 * s)
    algo_total = 2 * algo_w + algo_gap
    algo_top = int(h * 0.72)
    algo_btns = [
        Button(
            (
                w // 2 - algo_total // 2 + i * (algo_w + algo_gap),
                algo_top,
                algo_w,
                algo_h,
            ),
            label,
            value,
            int(22 * s),
        )
        for i, (value, label) in enumerate(ALGO_OPTIONS)
    ]
    start_w, start_h = int(340 * s), int(64 * s)
    start_btn = Button(
        (w // 2 - start_w // 2, int(h * 0.84), start_w, start_h),
        "MULAI GAME",
        "start",
        int(26 * s),
        bold=True,
    )

    def result():
        return {"maze": sel["maze"], "algorithm": sel["algorithm"]}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return result()
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    sel["maze"] = event.key - pygame.K_0
                if event.key in (pygame.K_b, pygame.K_TAB):
                    sel["algorithm"] = "astar" if sel["algorithm"] == "bfs" else "bfs"
            if back_btn.clicked(event):
                return "back"
            for card in cards:
                if card.clicked(event):
                    sel["maze"] = card.maze_id
            for b in algo_btns:
                if b.clicked(event):
                    sel["algorithm"] = b.value
            if start_btn.clicked(event):
                return result()

        screen.fill(C_BG)
        back_btn.draw(screen, fill=C_BACK_FILL)
        _text(
            screen,
            "PENGATURAN GAME",
            int(34 * s),
            C_TITLE,
            (w // 2, int(h * 0.07)),
            bold=True,
        )

        _text(
            screen,
            "PILIH MAP",
            int(22 * s),
            C_LABEL,
            (w // 2, int(h * 0.145)),
            bold=True,
        )
        for card in cards:
            card.draw(screen, active=(sel["maze"] == card.maze_id))

        _text(
            screen,
            "ALGORITMA MUSUH",
            int(22 * s),
            C_ENEMY_LABEL,
            (w // 2, int(h * 0.685)),
            bold=True,
        )
        for b in algo_btns:
            if sel["algorithm"] == b.value:
                b.draw(
                    screen,
                    fill=C_ENEMY_ACTIVE_FILL,
                    border=C_ENEMY_ACTIVE_BORDER,
                    border_w=4,
                )
            else:
                b.draw(screen)

        start_btn.draw(screen, fill=C_START_FILL)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    print("Hasil:", show_mulai(scr))
    pygame.quit()

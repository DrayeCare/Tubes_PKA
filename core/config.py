"""
FILE PENGATURAN (CONFIG)
Fungsi : Menyimpan semua konstanta, ukuran visual, warna (RGB/RGBA), path file maze, 
         algoritma AI, skenario pengujian, dan state permainan untuk Pac-Man: BFS vs A*.
Tugas  : Mengubah ukuran layar, warna, atau parameter simulasi langsung dari file ini.
         Seluruh modul/file lain akan mengimpor nilai-nilai dari file ini.
         
Cara pakai di file lain:
    from core import config
    pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
"""
import os

# ==============================================================================
# 1. GEOMETRI MAZE DAN UKURAN LAYAR
# (Sesuai Bab 3.1 & 3.2: Grid 2D 21x21 dengan tile berukuran 30 px)
# ==============================================================================
GRID_ROWS = 21
GRID_COLS = 21
TILE_SIZE = 30                          # Ukuran 1 kotak grid dalam piksel

MAZE_WIDTH = GRID_COLS * TILE_SIZE      # 630 piksel
MAZE_HEIGHT = GRID_ROWS * TILE_SIZE     # 630 piksel

# Bar Informasi / Heads-Up Display (HUD) di bagian bawah
HUD_HEIGHT = 60
SCREEN_WIDTH = MAZE_WIDTH               # Total lebar: 630 px
SCREEN_HEIGHT = MAZE_HEIGHT + HUD_HEIGHT # Total tinggi: 690 px (Maze 630 + HUD 60)

GAME_TITLE = "Pac-Man: BFS vs A* Search Pathfinding"

# ==============================================================================
# 2. MEKANIKA DAN KECEPATAN GAME
# (Sesuai Bab 3.1 & Bab 3.5: Pergerakan 4-arah & pengujian fair antara BFS & A*)
# ==============================================================================
FPS = 10  # Frame per second (kecepatan tick simulasi grid)

# Kecepatan karakter (1 tick = bergerak 1 kotak grid)
# Nilai dibuat sama untuk membandingkan BFS dan A* secara adil
PACMAN_MOVE_EVERY = 1
GHOST_MOVE_EVERY = 1

# ==============================================================================
# 3. LOGIKA MAZE GRID DAN DIRECTIONS
# (Sesuai Bab 3.2.2: Pergerakan 4-arah: Atas, Bawah, Kiri, Kanan. Tanpa diagonal)
# ==============================================================================
PATH = 0   # Sel berupa jalan yang dapat dilewati
WALL = 1   # Sel berupa dinding penghalang

# Arah pergerakan dalam bentuk koordinat (selisih_baris, selisih_kolom)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Tuple 4 arah pergerakan yang valid di dalam grid
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# ==============================================================================
# 4. PALET WARNA (RGB & RGBA)
# (Sesuai elemen visual Pac-Man, Ghost, Exit, Wall, dan Antarmuka HUD)
# ==============================================================================
COLOR_BG = (0, 0, 0)                # Hitam (Latar Maze)
COLOR_WALL = (33, 33, 222)          # Biru (Dinding Labirin)
COLOR_PATH = (0, 0, 0)              # Hitam (Jalan)
COLOR_PACMAN = (255, 255, 0)        # Kuning (Pac-Man)
COLOR_GHOST = (255, 0, 0)           # Merah (AI Ghost / Hantu)
COLOR_EXIT = (0, 200, 0)            # Hijau (Pintu Keluar / Exit)
COLOR_TEXT = (255, 255, 255)        # Putih (Teks Statistik/HUD)

# Warna UI & Menu
COLOR_HUD_BG = (20, 20, 20)         # Latar belakang HUD bawah
COLOR_WIN = (0, 220, 0)             # Teks/Status Menang
COLOR_LOSE = (230, 30, 30)          # Teks/Status Kalah
COLOR_BUTTON = (50, 50, 160)        # Tombol Menu
COLOR_BUTTON_HOVER = (90, 90, 220)  # Hover Tombol Menu
COLOR_OVERLAY = (0, 0, 0, 180)      # Transparansi Lapisan (RGBA)

# Radius visual lingkaran Pac-Man dan Ghost
CHARACTER_RADIUS = TILE_SIZE // 2 - 3
EXIT_MARGIN = 4                     # Margin batas kotak hijau Exit

# ==============================================================================
# 5. FONT DAN UKURAN TEKS
# ==============================================================================
FONT_NAME = None                    # None = Default Font Pygame
FONT_SIZE_TITLE = 48
FONT_SIZE_MENU = 28
FONT_SIZE_HUD = 20

# ==============================================================================
# 6. PENANGANAN PATH ASSET DAN BERKAS LABIRIN (JSON)
# (Sesuai Bab 3.2.3: Tiga jenis maze dengan tingkat kompleksitas berbeda)
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAZE_DIR = os.path.join(BASE_DIR, "mazes")

# Path file JSON untuk masing-masing maze
MAZE_FILES = {
    1: os.path.join(MAZE_DIR, "maze1.json"),
    2: os.path.join(MAZE_DIR, "maze2.json"),
    3: os.path.join(MAZE_DIR, "maze3.json"),
}

# Judul resmi maze sesuai Bab 3.2.3 proposal
MAZE_TITLES = {
    1: "Maze 1: Sedikit Belokan",
    2: "Maze 2: Banyak Belokan",
    3: "Maze 3: Memiliki Jalan Buntu",
}

# ==============================================================================
# 7. ALGORITMA PENGEJAR (SEARCH ALGORITHMS)
# (Sesuai Bab 2.5, 2.7, 3.4: Breadth-First Search dan A* Search)
# ==============================================================================
ALGO_BFS = "BFS"
ALGO_ASTAR = "A*"
ALGORITHMS = (ALGO_BFS, ALGO_ASTAR)

# ==============================================================================
# 8. SKENARIO PENGUJIEN & PARAMETER EVALUASI
# (Sesuai Bab 3.5 & Bab 3.6: Pengujian target Diam vs Bergerak)
# ==============================================================================
SCENARIO_STATIC = "Pac-Man Diam"
SCENARIO_MOVING = "Pac-Man Bergerak"
SCENARIOS = (SCENARIO_STATIC, SCENARIO_MOVING)

# ==============================================================================
# 9. STATE MACHINE / STATUS PERMAINAN
# ==============================================================================
STATE_MENU = "menu"
STATE_SELECT_MAZE = "select_maze"
STATE_PLAYING = "playing"
STATE_WIN = "win"
STATE_LOSE = "lose"

# ==============================================================================
# 10. TEKS NOTIFIKASI DAN PESAN PERMAINAN
# (Sesuai Bab 3.1 & 3.2.2: Syarat Kemenangan dan Kekalahan)
# ==============================================================================
TEXT_WIN = "MENANG! Pac-Man berhasil mencapai Exit"
TEXT_LOSE = "KALAH! Pac-Man tertangkap oleh Ghost"
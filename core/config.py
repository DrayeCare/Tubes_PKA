"""
FILE PENGATURAN (CONFIG)
Fungsi: Menyimpan semua angka dan warna dasar game.
Tugas: Jika dosen minta ganti warna Pac-Man atau ukuran layar, UBAH ANGKA DI SINI SAJA.
"""
# core/config.py

# Ukuran Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 10  # Kecepatan game (semakin kecil semakin lambat)

# Ukuran Grid
TILE_SIZE = 40

# Warna (RGB)
COLOR_BG = (0, 0, 0)          # Hitam
COLOR_WALL = (33, 33, 222)    # Biru
COLOR_PATH = (0, 0, 0)        # Hitam
COLOR_PACMAN = (255, 255, 0)  # Kuning
COLOR_GHOST = (255, 0, 0)     # Merah
COLOR_EXIT = (0, 255, 0)      # Hijau
COLOR_TEXT = (255, 255, 255)  # Putih
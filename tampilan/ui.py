"""
FILE TAMPILAN VISUAL (USER INTERFACE)
Fungsi: Menggambar kotak-kotak labirin, Pac-Man, Ghost, dan Exit ke layar.
Tugas: Rapikan tampilan game di sini (misal mau ganti bentuk Ghost, tambah teks skor, dll).
"""
import pygame
from core import config

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man AI: BFS vs A*")
    return screen

def render_game(screen, grid, pacman_pos, ghost_pos, exit_pos):
    screen.fill(config.COLOR_BG)
    
    # 1. Gambar Grid & Tembok
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            x = col_idx * config.TILE_SIZE
            y = row_idx * config.TILE_SIZE
            
            if cell == 1: # Tembok
                pygame.draw.rect(screen, config.COLOR_WALL, (x, y, config.TILE_SIZE, config.TILE_SIZE))

    # 2. Gambar Exit
    if exit_pos:
        ex_x = exit_pos[1] * config.TILE_SIZE
        ex_y = exit_pos[0] * config.TILE_SIZE
        pygame.draw.rect(screen, config.COLOR_EXIT, (ex_x, ex_y, config.TILE_SIZE, config.TILE_SIZE))

    # 3. Gambar Ghost
    gh_x = ghost_pos[1] * config.TILE_SIZE
    gh_y = ghost_pos[0] * config.TILE_SIZE
    pygame.draw.circle(screen, config.COLOR_GHOST, (gh_x + config.TILE_SIZE//2, gh_y + config.TILE_SIZE//2), config.TILE_SIZE//2 - 2)

    # 4. Gambar Pac-Man
    pc_x = pacman_pos[1] * config.TILE_SIZE
    pc_y = pacman_pos[0] * config.TILE_SIZE
    pygame.draw.circle(screen, config.COLOR_PACMAN, (pc_x + config.TILE_SIZE//2, pc_y + config.TILE_SIZE//2), config.TILE_SIZE//2 - 2)

    pygame.display.flip()


#Perubaan pada git
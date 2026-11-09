import pygame
import json
import time
from core.config import (
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    COLOR_BG, COLOR_WALL, COLOR_PATH, COLOR_PACMAN,
    COLOR_GHOST, COLOR_EXIT, COLOR_TEXT, GHOST_MOVE_DELAY
)
# Import fungsi algoritma pathfinding
from algoritma.bfs import bfs_search
from algoritma.astar import astar_search

class Game:
    def __init__(self, maze_path, algorithm="ASTAR"):
        """
        maze_path: Path ke file json (misal: 'mazes/maze1.json')
        algorithm: 'BFS' atau 'ASTAR'
        """
        self.algorithm = algorithm.upper()
        self.load_maze(maze_path)
        
        # Grid position setup [row, col]
        self.pacman_pos = list(self.maze_data["pacman_start"])
        self.ghost_pos = list(self.maze_data["ghost_start"])
        self.exit_pos = list(self.maze_data["exit"])
        self.grid = self.maze_data["grid"]
        
        # State permainan
        self.state = "PLAYING"  # 'PLAYING', 'WIN', 'GAME_OVER'
        self.ghost_last_move_time = pygame.time.get_ticks()
        
        # Metrik performa untuk pengujian proposal
        self.nodes_explored = 0
        self.last_search_time = 0.0
        self.current_path = []
        
        # Hitung jalur awal untuk hantu
        self.update_ghost_path()

    def load_maze(self, filepath):
        with open(filepath, 'r') as f:
            self.maze_data = json.load(f)

    def update_ghost_path(self):
        """Memanggil algoritma pencarian sesuai pilihan (BFS/A*)"""
        start_time = time.perf_counter()
        
        start = tuple(self.ghost_pos)
        target = tuple(self.pacman_pos)
        
        if self.algorithm == "BFS":
            path, nodes = bfs_search(self.grid, start, target)
        else:
            path, nodes = astar_search(self.grid, start, target)
            
        self.last_search_time = time.perf_counter() - start_time
        self.nodes_explored = nodes
        
        # Path mengembalikan daftar koordinat [(r1, c1), (r2, c2), ...]
        # Simpan jalur (abaikan posisi awal hantu)
        self.current_path = path[1:] if len(path) > 1 else []

    def handle_input(self, event):
        """Grid-based movement untuk Pac-Man menggunakan keyboard"""
        if self.state != "PLAYING":
            return

        if event.type == pygame.KEYDOWN:
            new_row, new_col = self.pacman_pos[0], self.pacman_pos[1]
            
            if event.key in (pygame.K_UP, pygame.K_w):
                new_row -= 1
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                new_row += 1
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                new_col -= 1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                new_col += 1
            else:
                return

            # Validasi pergerakan: Tidak menabrak dinding (1)
            if self.is_valid_move(new_row, new_col):
                self.pacman_pos = [new_row, new_col]
                # Hitung ulang jalur hantu saat Pac-Man berpindah sel
                self.update_ghost_path()
                self.check_game_conditions()

    def is_valid_move(self, row, col):
        rows = len(self.grid)
        cols = len(self.grid[0])
        if 0 <= row < rows and 0 <= col < cols:
            return self.grid[row][col] != 1
        return False

    def update(self):
        """Logika pergerakan Ghost berbasis waktu"""
        if self.state != "PLAYING":
            return

        now = pygame.time.get_ticks()
        if now - self.ghost_last_move_time >= GHOST_MOVE_DELAY:
            self.ghost_last_move_time = now
            
            if self.current_path:
                next_step = self.current_path.pop(0)
                self.ghost_pos = list(next_step)
                self.check_game_conditions()

    def check_game_conditions(self):
        """Memeriksa Win condition (Exit) & Game Over condition (Ghost)"""
        # Game Over: Hantu dan Pac-Man di petak yang sama
        if self.pacman_pos == self.ghost_pos:
            self.state = "GAME_OVER"
        # Win: Pac-Man mencapai pintu keluar
        elif self.pacman_pos == self.exit_pos:
            self.state = "WIN"

    def render(self, surface):
        """Draw Grid, Exit, Pac-Man, Ghost, dan Overlay Game Over/Win"""
        surface.fill(COLOR_BG)
        
        # 1. Render Grid & Exit
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.grid[r][c] == 1:
                    pygame.draw.rect(surface, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(surface, COLOR_PATH, rect, 1)

        # Draw Exit Portal
        exit_r, exit_c = self.exit_pos
        exit_rect = pygame.Rect(exit_c * TILE_SIZE + 4, exit_r * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        pygame.draw.rect(surface, COLOR_EXIT, exit_rect, border_radius=6)

        # 2. Render Pac-Man (Kuning)
        pac_r, pac_c = self.pacman_pos
        center_pac = (pac_c * TILE_SIZE + TILE_SIZE // 2, pac_r * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(surface, COLOR_PACMAN, center_pac, TILE_SIZE // 2 - 3)

        # 3. Render Ghost (Merah)
        ghost_r, ghost_c = self.ghost_pos
        center_ghost = (ghost_c * TILE_SIZE + TILE_SIZE // 2, ghost_r * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(surface, COLOR_GHOST, center_ghost, TILE_SIZE // 2 - 3)

        # 4. Render State Overlay (Win / Game Over)
        if self.state in ("WIN", "GAME_OVER"):
            self.render_end_screen(surface)

    def render_end_screen(self, surface):
        font = pygame.font.SysFont(None, 48)
        sub_font = pygame.font.SysFont(None, 24)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        surface.blit(overlay, (0, 0))

        title_text = "PAC-MAN ESCAPED!" if self.state == "WIN" else "GAME OVER!"
        title_color = COLOR_EXIT if self.state == "WIN" else COLOR_GHOST
        
        text_surface = font.render(title_text, True, title_color)
        rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        surface.blit(text_surface, rect)

        prompt_surface = sub_font.render("Tekan [ESC] atau [ENTER] untuk kembali ke Menu Utama", True, COLOR_TEXT)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        surface.blit(prompt_surface, prompt_rect)


def run_game(screen, maze_path, algorithm):
    """Function wrapper untuk dipanggil dari main_menu.py"""
    clock = pygame.time.Clock()
    game = Game(maze_path, algorithm)
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            
            if game.state == "PLAYING":
                game.handle_input(event)
            else:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return "MENU"

        game.update()
        game.render(screen)
        pygame.display.flip()
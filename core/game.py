import json
import pygame

from algoritma.astar import cari_jalur_astar
from algoritma.bfs import cari_jalur_bfs
from core import config
from tampilan.ui_setting import get_movement_keys # Ubah jadi ui_setting jika sudah rename

SEARCH = {"bfs": cari_jalur_bfs, "astar": cari_jalur_astar}

class Game:
    def __init__(self, maze_path, algorithm="astar"):
        self.algorithm = algorithm.lower()
        self.search_func = SEARCH.get(self.algorithm, cari_jalur_astar)
        
        with open(maze_path, "r") as f:
            self.maze_data = json.load(f)

        self.grid = self.maze_data["grid"]
        self.pacman_pos = list(self.maze_data["pacman_start"])
        self.ghost_pos = list(self.maze_data["ghost_start"])
        self.exit_pos = list(self.maze_data["exit"])

        self.state = config.STATE_PLAYING 
        self.ghost_last_move_time = pygame.time.get_ticks()

        self.total_nodes = 0
        self.total_time = 0.0
        self.search_count = 0
        self.last_path_length = 0
        self.current_path = []

        # Setup Kontrol (WASD & Panah)
        self.key_dir = {
            pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0), pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1),
            pygame.K_w: (-1, 0), pygame.K_s: (1, 0), pygame.K_a: (0, -1), pygame.K_d: (0, 1)
        }
        
        # Coba ambil dari setting jika fungsinya ada
        try:
            keys = get_movement_keys()
            if isinstance(keys, dict) and "up" in keys:
                self.key_dir = {}
                for k in keys["up"]: self.key_dir[k] = (-1, 0)
                for k in keys["down"]: self.key_dir[k] = (1, 0)
                for k in keys["left"]: self.key_dir[k] = (0, -1)
                for k in keys["right"]: self.key_dir[k] = (0, 1)
        except Exception:
            pass

        self.update_ghost_path()

    def update_ghost_path(self):
        start = tuple(self.ghost_pos)
        target = tuple(self.pacman_pos)
        path, nodes, elapsed = self.search_func(self.grid, start, target)
        
        self.total_nodes += nodes
        self.total_time += elapsed
        self.search_count += 1
        
        self.last_path_length = max(len(path) - 1, 0)
        self.current_path = path[1:] if len(path) > 1 else []

    def get_stats(self):
        n = max(self.search_count, 1)
        return {
            "search_time_ms": (self.total_time / n) * 1000,
            "nodes_explored": int(self.total_nodes / n),
            "path_length": self.last_path_length
        }

    @property
    def winner(self):
        return "pacman" if self.state == config.STATE_WIN else "ghost"

    def handle_input(self, event):
        if self.state != config.STATE_PLAYING or event.type != pygame.KEYDOWN:
            return
        if event.key in self.key_dir:
            dr, dc = self.key_dir[event.key]
            nr, nc = self.pacman_pos[0] + dr, self.pacman_pos[1] + dc
            if self.is_valid_move(nr, nc):
                self.pacman_pos = [nr, nc]
                self.update_ghost_path()
                self.check_game_conditions()

    def is_valid_move(self, r, c):
        return (0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]) and self.grid[r][c] != 1)

    def update(self):
        if self.state != config.STATE_PLAYING:
            return
        now = pygame.time.get_ticks()
        if now - self.ghost_last_move_time >= config.GHOST_MOVE_DELAY * 1000:
            self.ghost_last_move_time = now
            if self.current_path:
                self.ghost_pos = list(self.current_path.pop(0))
                self.check_game_conditions()

    def check_game_conditions(self):
        if self.pacman_pos == self.exit_pos:
            self.state = config.STATE_WIN
        elif self.pacman_pos == self.ghost_pos:
            self.state = config.STATE_LOSE

    def render(self, screen):
        screen.fill(config.COLOR_BG)
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                rect = pygame.Rect(c * config.TILE_SIZE, r * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE)
                if self.grid[r][c] == 1:
                    pygame.draw.rect(screen, config.COLOR_WALL, rect)
                else:
                    pygame.draw.rect(screen, config.COLOR_PATH, rect, 1)
                    
        er, ec = self.exit_pos
        pygame.draw.rect(screen, config.COLOR_EXIT, (ec*config.TILE_SIZE+4, er*config.TILE_SIZE+4, config.TILE_SIZE-8, config.TILE_SIZE-8), border_radius=6)
        
        pr, pc = self.pacman_pos
        pygame.draw.circle(screen, config.COLOR_PACMAN, (pc*config.TILE_SIZE+config.TILE_SIZE//2, pr*config.TILE_SIZE+config.TILE_SIZE//2), config.TILE_SIZE//2-3)
        
        gr, gc = self.ghost_pos
        pygame.draw.circle(screen, config.COLOR_GHOST, (gc*config.TILE_SIZE+config.TILE_SIZE//2, gr*config.TILE_SIZE+config.TILE_SIZE//2), config.TILE_SIZE//2-3)


def run_game(screen, game):
    clock = pygame.time.Clock()
    while game.state == config.STATE_PLAYING:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            game.handle_input(event)
            
        game.update()
        game.render(screen)
        pygame.display.flip()
        
    return "finished"
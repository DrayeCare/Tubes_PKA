"""
FILE MESIN UTAMA (GAME ENGINE)
Fungsi: Otak dari game. Mengatur input keyboard, memanggil AI (BFS/A*), dan cek menang/kalah.
Tugas: Lengkapi bagian logika input keyboard di dalam fungsi jalankan_game().
"""
import pygame
import json
import sys
from core import config
from core import recorder
from tampilan import ui
from algoritma import bfs, astar

def load_maze(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def jalankan_game(maze_file="mazes/maze1.json", algoritma_pilihan="astar"):
    screen = ui.init_pygame()
    clock = pygame.time.Clock()
    
    # Load Data Maze
    maze_data = load_maze(maze_file)
    grid = maze_data["grid"]
    pacman_pos = list(maze_data["pacman_start"])
    ghost_pos = list(maze_data["ghost_start"])
    exit_pos = list(maze_data["exit"])
    
    rec = recorder.Recorder()
    running = True

    while running:
        clock.tick(config.FPS)
        
        # 1. Cek Event (Input Keyboard / Tutup Game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # TODO: Tambahkan logika input keyboard Pac-Man di sini
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP: ... cek apakah menabrak dinding (1), jika tidak pacman_pos[0] -= 1
            
        # Simpan gerakan Pac-Man
        rec.rekam_langkah(tuple(pacman_pos))
        
        # 2. Panggil Algoritma AI (Ghost mengejar)
        if algoritma_pilihan == "bfs":
            path, nodes, time_taken = bfs.cari_jalur_bfs(grid, tuple(ghost_pos), tuple(pacman_pos))
        else:
            path, nodes, time_taken = astar.cari_jalur_astar(grid, tuple(ghost_pos), tuple(pacman_pos))
        
        # 3. Gerakkan Ghost (Ambil langkah pertama dari path yang dihasilkan AI)
        if path and len(path) > 1:
            ghost_pos = list(path[1]) 
            
        # 4. Cek Kondisi Menang / Kalah
        if ghost_pos == pacman_pos:
            print("GAME OVER! Ghost menangkap Pac-Man.")
            running = False
        elif pacman_pos == exit_pos:
            print("YOU WIN! Pac-Man sampai di Exit.")
            running = False

        # 5. Gambar ke Layar
        ui.render_game(screen, grid, pacman_pos, ghost_pos, exit_pos)

    pygame.quit()
    sys.exit()
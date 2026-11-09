import csv
import json
from core import config
from algoritma import astar, bfs

def jalankan_eksperimen():
    hasil = []
    
    # Gunakan config.MAZE_FILES agar path selalu benar di mana pun dijalankan
    for maze_id, maze_path in config.MAZE_FILES.items():
        with open(maze_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        grid = data["grid"]
        start = tuple(data["ghost_start"])
        goal = tuple(data["pacman_start"])
        
        # Uji BFS
        p_bfs, n_bfs, t_bfs = bfs.cari_jalur_bfs(grid, start, goal)
        hasil.append(["BFS", config.MAZE_TITLES[maze_id], max(len(p_bfs)-1, 0), n_bfs, round(t_bfs, 5)])
        
        # Uji A*
        p_as, n_as, t_as = astar.cari_jalur_astar(grid, start, goal)
        hasil.append(["A*", config.MAZE_TITLES[maze_id], max(len(p_as)-1, 0), n_as, round(t_as, 5)])

    # Tambahkan encoding="utf-8" untuk mencegah error karakter di Windows
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritma", "Maze", "Path Length", "Nodes Explored", "Time (s)"])
        writer.writerows(hasil)
    
    print("✅ Eksperimen selesai! Cek file 'results.csv' di root folder.")

if __name__ == "__main__":
    jalankan_eksperimen()
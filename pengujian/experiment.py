import csv
import json
from algoritma import astar, bfs

def jalankan_eksperimen():
    mazes = ["maze1.json", "maze2.json", "maze3.json"]
    hasil = []

    for m in mazes:
        with open(f"mazes/{m}", "r") as f:
            data = json.load(f)
        
        grid = data["grid"]
        start = tuple(data["ghost_start"])
        goal = tuple(data["pacman_start"])

        # Uji BFS
        p_bfs, n_bfs, t_bfs = bfs.cari_jalur_bfs(grid, start, goal)
        hasil.append(["BFS", m, max(len(p_bfs)-1, 0), n_bfs, round(t_bfs, 5)])

        # Uji A*
        p_as, n_as, t_as = astar.cari_jalur_astar(grid, start, goal)
        hasil.append(["A*", m, max(len(p_as)-1, 0), n_as, round(t_as, 5)])

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritma", "Maze", "Path Length", "Nodes Explored", "Time (s)"])
        writer.writerows(hasil)

    print("Eksperimen selesai! Cek results.csv")

if __name__ == "__main__":
    jalankan_eksperimen()
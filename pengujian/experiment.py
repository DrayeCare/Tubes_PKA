"""
FILE PENGUJIAN OTOMATIS
Fungsi: Menjalankan BFS & A* secara otomatis tanpa buka jendela game, lalu menyimpan hasilnya ke Excel (CSV).
Tugas: Jalankan file ini untuk mendapatkan data perbandingan buat Laporan Bab 4.
"""
import json
import csv
from algoritma import bfs, astar

def jalankan_eksperimen():
    # Load Maze
    with open('mazes/maze1.json', 'r') as f:
        data = json.load(f)
        
    grid = data["grid"]
    start = tuple(data["ghost_start"])
    goal = tuple(data["pacman_start"])
    
    hasil = []
    
    # Uji BFS
    path_bfs, nodes_bfs, time_bfs = bfs.cari_jalur_bfs(grid, start, goal)
    hasil.append(["BFS", "Maze 1", len(path_bfs), nodes_bfs, time_bfs])
    
    # Uji A*
    path_astar, nodes_astar, time_astar = astar.cari_jalur_astar(grid, start, goal)
    hasil.append(["A*", "Maze 1", len(path_astar), nodes_astar, time_astar])
    
    # Simpan ke CSV
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritma", "Maze", "Path Length", "Nodes Explored", "Time (s)"])
        writer.writerows(hasil)
        
    print("Eksperimen selesai! Cek results.csv")

if __name__ == "__main__":
    jalankan_eksperimen()
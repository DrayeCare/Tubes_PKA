"""
FILE ALGORITMA A* (A-STAR)
Fungsi: Mencari jalan terpendek dengan bantuan "kompas" (Heuristik Manhattan).
Tugas: Lengkapi logika A* di dalam fungsi cari_jalur_astar().
"""
import time
import heapq

def heuristik_manhattan(posisi_sekarang, target):
    # Rumus Manhattan Distance: |x1 - x2| + |y1 - y2|
    return abs(posisi_sekarang[0] - target[0]) + abs(posisi_sekarang[1] - target[1])

def cari_jalur_astar(grid, start, goal):
    """
    Mencari jalur menggunakan A*.
    Return: (path_list, nodes_explored, time_taken)
    """
    start_time = time.perf_counter()
    
    # TODO: Tulis algoritma A* di sini
    # 1. Gunakan heapq (Priority Queue)
    # 2. f(n) = g(n) + h(n)
    # 3. h(n) pakai fungsi heuristik_manhattan di atas
    
    # --- KODE DUMMY (Hapus dan ganti dengan A* asli) ---
    path = [start, goal]
    nodes_explored = 5
    # ----------------------------------------------------

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    
    return path, nodes_explored, time_taken
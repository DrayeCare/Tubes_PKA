"""
FILE ALGORITMA BFS (BREADTH-FIRST SEARCH)
Fungsi: Mencari jalan terpendek dari Ghost ke Pac-Man dengan cara "menyebar rata".
Tugas: Lengkapi logika BFS di dalam fungsi cari_jalur_bfs().
"""

import time


def cari_jalur_bfs(grid, start, goal):
    """
    Mencari jalur menggunakan BFS.
    Return: (path_list, nodes_explored, time_taken)
    """
    start_time = time.perf_counter()

    # TODO: Tulis algoritma BFS di sini
    # 1. Gunakan deque untuk antrean (queue)
    # 2. Simpan parent (jejak sebelumnya) untuk melacak jalur
    # 3. Cek tetangga (atas, bawah, kiri, kanan) yang bukan tembok (1)

    # --- KODE DUMMY (Hapus dan ganti dengan BFS asli) ---
    path = [start, goal]
    nodes_explored = 10
    # ----------------------------------------------------

    end_time = time.perf_counter()
    time_taken = end_time - start_time

    return path, nodes_explored, time_taken

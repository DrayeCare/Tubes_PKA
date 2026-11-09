import time
from collections import deque

def cari_jalur_bfs(grid, start, goal):
    start_time = time.perf_counter()
    if start == goal:
        return [start], 1, time.perf_counter() - start_time

    baris, kolom = len(grid), len(grid[0])
    antrean = deque([start])
    sudah_dikunjungi = {start}
    induk = {start: None}
    nodes_explored = 0

    while antrean:
        sekarang = antrean.popleft()
        nodes_explored += 1

        if sekarang == goal:
            jalur = []
            node = sekarang
            while node is not None:
                jalur.append(node)
                node = induk[node]
            jalur.reverse()
            return jalur, nodes_explored, time.perf_counter() - start_time

        r, c = sekarang
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < baris and 0 <= nc < kolom and grid[nr][nc] != 1:
                tetangga = (nr, nc)
                if tetangga not in sudah_dikunjungi:
                    sudah_dikunjungi.add(tetangga)
                    induk[tetangga] = sekarang
                    antrean.append(tetangga)

    return [], nodes_explored, time.perf_counter() - start_time
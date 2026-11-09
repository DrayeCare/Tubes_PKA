"""
FILE PINTU MASUK (ENTRY POINT)
Fungsi: Titik awal program dijalankan.
Tugas: Tekan tombol "Run" (F5) di file ini untuk memulai game.
Kalian bisa ubah nama maze atau algoritma yang mau di-test di sini.
"""

from core import game

if __name__ == "__main__":
    print("Menjalankan Game Pac-Man AI...")
    # Ubah maze_file menjadi "mazes/maze2.json" atau "mazes/maze3.json" untuk ganti labirin
    # Ubah algoritma_pilihan menjadi "bfs" atau "astar" untuk ganti AI Ghost
    game.jalankan_game(maze_file="mazes/maze1.json", algoritma_pilihan="astar")

    # Firaz Dan Waiz

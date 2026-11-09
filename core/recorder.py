"""
FILE PEREKAM GERAKAN
Fungsi: Mencatat setiap langkah Pac-Man (seperti CCTV) untuk keperluan pengujian/replay.
Tugas: Tidak perlu diubah, biarkan saja.
"""


class Recorder:
    def __init__(self):
        self.history_moves = []

    def rekam_langkah(self, posisi_pacman):
        # Menyimpan posisi (row, col) ke dalam list
        self.history_moves.append(posisi_pacman)

    def dapatkan_rekaman(self):
        return self.history_moves

    def reset(self):
        self.history_moves = []

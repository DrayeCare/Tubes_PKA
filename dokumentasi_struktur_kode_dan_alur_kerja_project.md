# Dokumentasi Arsitektur Kode & Alur Kerja Program
**Proyek Tugas Besar PKA: Analisis Perbandingan BFS vs A* pada AI Pengejar Pac-Man**

Dokumen ini berisi penjelasan detail mengenai fungsi dari setiap modul/file di dalam proyek serta bagaimana alur kerja (*workflow*) dari sistem yang telah dibuat.

---

## 1. Struktur Direktori Proyek

Berikut adalah gambaran umum struktur direktori dan file dalam repositori `DrayeCare-Tubes_PKA`:

```text
DrayeCare-Tubes_PKA/
├── algoritma/
│   ├── __init__.py
│   ├── astar.py          # Implementasi Algoritma A* (A-Star)
│   └── bfs.py            # Implementasi Algoritma Breadth-First Search (BFS)
├── core/
│   ├── __init__.py
│   ├── config.py         # Konfigurasi global (Ukuran grid, warna, FPS, dll.)
│   ├── game.py           # Logika utama permainan (Game Engine & Loop)
│   └── recorder.py       # Pencatat metrik pengujian (Waktu, Nodes, Path Length)
├── mazes/
│   ├── maze1.json        # Labirin 1: Sedikit Belokan
│   ├── maze2.json        # Labirin 2: Banyak Belokan
│   └── maze3.json        # Labirin 3: Memiliki Jalan Buntu
├── pengujian/
│   ├── __init__.py
│   └── experiment.py     # Script benchmarking / pengujian otomatis (Batch Run)
├── tampilan/
│   ├── __init__.py
│   └── ui.py             # Rendering visual GUI permainan (Pygame/Tkinter)
├── main.py               # Entry point untuk menjalankan game secara interaktif
└── readme.md             # Petunjuk umum penggunaan proyek
```

---

## 2. Penjelasan Detail Setiap File

### 📁 `algoritma/` (Modul Core AI & Pathfinding)

#### `algoritma/bfs.py`
* **Fungsi:** Mengimplementasikan pencarian jalur *Breadth-First Search* (Uninformed Search).
* **Peran Utama:**
  * Mencari rute dari posisi Ghost (start) ke Pac-Man (target) menggunakan struktur data antrean (`collections.deque`).
  * Mengeksplorasi tetangga sel (atas, bawah, kiri, kanan) secara menyeluruh per tingkat kedalaman.
  * Menghitung dan mengembalikan:
    1. **Jalur (*Path*):** Daftar koordinat `(x, y)` dari start ke target.
    2. **Nodes Explored:** Jumlah total simpul/grid yang di-`pop` dari antrean selama pencarian.
    3. **Search Time:** Waktu komputasi pencarian (dalam milidetik/detik).

#### `algoritma/astar.py`
* **Fungsi:** Mengimplementasikan pencarian jalur $A^*$ (*Informed Search*) menggunakan fungsi evaluasi $f(n) = g(n) + h(n)$.
* **Peran Utama:**
  * Menggunakan struktur data *Priority Queue* (`heapq`) untuk memprioritaskan node dengan nilai $f(n)$ terkecil.
  * Menggunakan **Manhattan Distance** sebagai fungsi heuristik $h(n)$:
    $$h(n) = |x_1 - x_2| + |y_1 - y_2|$$
  * Menghitung biaya perjalanan $g(n)$ dari awal ke node saat ini.
  * Mengembalikan daftar jalur, jumlah *nodes explored*, dan *search time*.

---

### 📁 `core/` (Modul Logika & Konfigurasi Sistem)

#### `core/config.py`
* **Fungsi:** Menyimpan konstanta dan konfigurasi global permainan.
* **Isi Utama:**
  * Ukuran grid (misal: 20x20 sel, ukuran sel dalam piksel).
  * Dimensi jendela layar (Window Width & Height).
  * Pengaturan warna standar (Hitam untuk dinding, Putih untuk jalur, Kuning untuk Pac-Man, Merah untuk Ghost, Biru untuk Exit).
  * Pengaturan FPS (Frames Per Second) dan kontrol kecepatan gerak karakter.

#### `core/game.py`
* **Fungsi:** Komponen *Game Engine* utama yang mengatur state permainan.
* **Peran Utama:**
  * Mengelola status karakter: posisi koordinat Pac-Man dan Ghost.
  * Membaca kondisi labirin (mana dinding, mana jalan).
  * Mengatur *Game Loop*: update posisi Pac-Man berdasarkan masukan keyboard pemain, dan update posisi Ghost berdasarkan algoritma terpilih.
  * **Fitur Autorepathing:** Mendeteksi jika Pac-Man berpindah grid. Jika posisi Pac-Man berubah, `game.py` memanggil ulang algoritma (`bfs` atau `astar`) untuk memperbarui jalur pencarian Ghost secara *real-time*.
  * Mendeteksi kondisi menang (Pac-Man mencapai Exit) dan kalah (Ghost menabrak Pac-Man).

#### `core/recorder.py`
* **Fungsi:** Instrumen pengumpul data statistik/metrik pengujian.
* **Peran Utama:**
  * Mencatat setiap sesi pencarian jalur (waktu eksekusi, jumlah node yang dibuka, panjang jalur yang terbentuk).
  * Menghitung akumulasi statistik per permainan (rata-rata waktu pencarian per *step*, total pencarian ulang / *repath count*, total durasi permainan).
  * Menyimpan log hasil pengujian ke format data yang mudah dianalisis (misal: array/JSON/CSV).

---

### 📁 `mazes/` (Data Labirin JSON)

#### `mazes/maze1.json`, `maze2.json`, `maze3.json`
* **Fungsi:** Menyimpan struktur layout labirin dalam format JSON.
* **Isi Data:**
  * Array matriks 2D (nilai `1` untuk Dinding, `0` untuk Jalan yang bisa dilewati).
  * Posisi spawn awal Pac-Man: `[x_pacman, y_pacman]`.
  * Posisi spawn awal Ghost: `[x_ghost, y_ghost]`.
  * Posisi koordinat Exit: `[x_exit, y_exit]`.
* **Karakteristik Labirin:**
  * **Maze 1:** Jalur terbuka, sedikit belokan.
  * **Maze 2:** Jalur rumit dengan banyak belokan mendadak.
  * **Maze 3:** Jalur dengan beberapa celah jalan buntu (*dead-end*).

---

### 📁 `tampilan/` (GUI User Interface)

#### `tampilan/ui.py`
* **Fungsi:** Mengurus pembuatan antarmuka grafis dan penggambaran (rendering).
* **Peran Utama:**
  * Menggambar matriks labirin, karakter Pac-Man, Ghost, dan titik Exit ke layar window.
  * Menyediakan menu awal (*Launcher*) untuk memilih:
    1. Pilihan Labirin (Maze 1, Maze 2, atau Maze 3).
    2. Pilihan Algoritma AI Pengejar (BFS vs $A^*$).
    3. Mode Pac-Man (Diam / Controlled Keyboard).
  * Menampilkan informasi HUD (*Heads-Up Display*) seperti algoritma aktif, waktu eksekusi *real-time*, dan statistik node di pojok layar GUI.

---

### 📁 `pengujian/` (Modul Automated Benchmarking)

#### `pengujian/experiment.py`
* **Fungsi:** Skrip pengujian otomatis tanpa perlu memainkan GUI manual.
* **Peran Utama:**
  * Mengakses seluruh kombinasi pengujian:
    * **3 Maze** $\times$ **2 Algoritma (BFS vs A\*)** $\times$ **2 Skenario (Pac-Man Diam vs Moving)**.
  * Menjalankan simulasi beberapa kali (*iterations*) untuk mendapatkan hasil rata-rata yang stabil secara saintifik.
  * Memastikan urutan pergerakan Pac-Man pada skenario bergerak bersifat *deterministic* (sama persis antara BFS dan A*) agar *apple-to-apple comparison*.
  * Meng-export data pengujian ke file laporan CSV/Excel untuk diolah pada Bab IV Laporan Akhir.

---

### 📄 File Utama Root

#### `main.py`
* **Fungsi:** titik masuk utama (*Entry Point*) program.
* **Peran Utama:** Menjalankan inisialisasi aplikasi, mengarahkan ke menu interaktif `tampilan/ui.py`, serta memulai game loop `core/game.py`.

---

## 3. Alur Kerja Sistem (Workflow)

```
                       [ PEMAIN / USER ]
                               │
                               ▼
                        1. Jalankan main.py
                               │
                               ▼
                   2. Tampil Menu UI (ui.py)
              ┌────────────────┴────────────────┐
              ▼                                 ▼
      Pilih Maze (1/2/3)              Pilih Algoritma (BFS/A*)
              └────────────────┬────────────────┘
                               │
                               ▼
                   3. Game Engine (game.py)
               Memuat JSON dari mazes/ & Config
                               │
                               ▼
                  4. Game Loop Utama Berjalan
               ┌───────────────┴───────────────┐
               ▼                               ▼
       Pemain gerakkan                 Ghost minta jalur
       Pac-Man (Keyboard)              ke Module Algoritma
               │                               │
               │                               ▼
               │                     Menjalankan bfs.py / astar.py
               │                     - Hitung Path
               │                     - Catat Search Time
               │                     - Hitung Nodes Explored
               │                               │
               └───────────────┬───────────────┘
                               │
                               ▼
                   5. Autorepath Check (game.py)
               Apakah Posisi Pac-Man Berubah?
              ├── YA  ──> Trigger Re-calculation (Panggil Algoritma Lagi)
              └── TIDAK ──> Ghost Lanjut Ikut Jalur Lama
                               │
                               ▼
                    6. Recording (recorder.py)
               Mencatat statistik pergerakan & pencarian
                               │
                               ▼
                    7. Kondisi Akhir Game
              ├── Pac-Man Capai Exit ──> PAC-MAN WIN
              └── Ghost Tangkap Pac-Man ──> GHOST WIN
```

---

## 4. Alur Kerja Modul Pengujian Otomatis (`experiment.py`)

Jika pengujian dilakukan untuk analisis data tugas besar (Bab IV):

1. Developer menjalankan `python -m pengujian.experiment`.
2. `experiment.py` mengiterasi kombinasi parameter:
   - Maze: `[Maze 1, Maze 2, Maze 3]`
   - Algoritma: `[BFS, A*]`
   - Kondisi: `[Static Target, Moving Target]`
3. Untuk setiap iterasi, program menjalankan pencarian tanpa menampilkan jendela GUI (Headless Mode) agar eksekusi cepat.
4. `recorder.py` mengumpulkan data setiap langkah.
5. Hasil akhir dirangkum dan disimpan otomatis ke berkas `pengujian_result.csv` untuk kemudian disajikan dalam bentuk tabel dan grafik perbandingan.
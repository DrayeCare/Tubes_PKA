# GAME DESIGN DOCUMENT (GDD)

**Judul Proyek:** Analisis Perbandingan Kinerja Algoritma Breadth-First Search (BFS) dan $A^*$ pada AI Pengejar dalam Permainan Pac-Man

**Mata Kuliah:** Pengantar Kecerdasan Artifisial

**Institusi:** Institut Teknologi Kalimantan — Fakultas Sains dan Teknologi Informasi (Program Studi Informatika)

**Dosen Pengampu:** Bima Prihasto, S.Si., M.Si., Ph.D.

**Disusun Oleh (Kelompok 5-B):**

* Anivah Mu'athiyah (11251064)


* Remarsya Fredericha (11251078)


* Andi Firaz Nadhir Baihaqi (11251086)


* Daniel Phillip Limbhoro (11251092)


* Huwaiza Ahmad Azfa (11251094)



---

## 1. Executive Summary & Core Concept

* **Nama Game:** Pac-Man: AI Search Benchmark (Pac-Man Sederhana)


* **Genre:** 2D Grid-Based Arcade / Puzzle & Pathfinding Simulation


* **Platform:** PC / Desktop (Keyboard Control)


* **Target Audiens:** Mahasiswa, Akademisi, dan Developer Game yang tertarik pada implementasi algoritma kecerdasan buatan (*pathfinding*).


* **Core Loop:**
1. Pemain memilih salah satu dari 3 tipe *maze* dan menentukan algoritma AI pengejar (BFS atau $A^*$).


2. Pemain mengendalikan Pac-Man menuju pintu keluar (*exit*).


3. AI Hantu (*Ghost*) secara kontinu/berkala menghitung rute terpendek dan mengejar Pac-Man.


4. Sesi berakhir **MENANG** jika Pac-Man mencapai *exit*, atau **KALAH** jika Pac-Man tertangkap *ghost*.





---

## 2. Gameplay Mechanics & Game Rules

### Karakter & Entitas Game



1. **Pac-Man (Player Character):**


* Dikendalikan manual via keyboard (tombol arah/panah).


* Bergerak 4 arah (Atas, Bawah, Kiri, Kanan) pada sistem *grid* 2D. Tidak ada pergerakan diagonal.


* Misi: Mencapai posisi pintu keluar (*exit*).




2. **Ghost / Hantu (AI Character):**


* Dikendalikan penuh oleh Agen AI.


* Mencari dan menelusuri jalur menuju posisi Pac-Man menggunakan algoritma pencarian pilihan pemain (BFS atau $A^*$).




3. **Elemen Lingkungan:**


* **Jalur (Tile Bebas):** Kotak grid yang dapat dilalui karakter.


* **Dinding (Obstacle):** Kotak grid yang menghalangi pergerakan.


* **Exit (Pintu Keluar):** Titik tujuan akhir Pac-Man untuk memenangkan permainan.





### Aturan Permainan (Game Rules)



* Karakter tidak dapat melompati atau menembus dinding.


* Pergerakan terbatas pada 4 arah mata angin (non-diagonal) dengan *step cost* homogen ($g(n) = 1$ per langkah).


* **Kondisi Menang (*Victory Condition*):** Pac-Man mencapai koordinat *exit* sebelum tertangkap Hantu.


* **Kondisi Kalah (*Defeat Condition*):** Koordinat Hantu sama dengan koordinat Pac-Man (tertangkap) sebelum Pac-Man mencapai *exit*.



---

## 3. Level & Maze Design

Permainan menyediakan 3 variasi *maze* dua dimensi untuk menguji ketahanan dan kinerja algoritma pada konfigurasi geografis ruang pencarian yang berbeda:

| Nama Level | Karakteristik Geometric Maze | Tujuan Pengujian AI |
| --- | --- | --- |
| **Maze 1: Sedikit Belokan** | Area relatif terbuka dengan hambatan koridor minimal.

 | Memeriksa performa pada pencarian jalur langsung tanpa banyak rintangan kompleks.

 |
| **Maze 2: Banyak Belokan** | Koridor berkelok-kelok tajam dan padat rintangan.

 | Memeriksa ekspansi simpul pada ruang yang mengharuskan navigasi melingkar.

 |
| **Maze 3: Jalan Buntu** | Memiliki beberapa cabang lorong mati (*dead-ends*).

 | Memuji efisiensi evaluasi heuristik agar AI tidak terjebak menjelajahi lorong buntu.

 |

Setiap maze telah memiliki koordinat awal Pac-Man, koordinat awal Ghost, dan lokasi Exit yang tetap.

---

## 4. Artificial Intelligence (AI) Specification & PEAS Framework

### Kerangka PEAS Agen AI (Ghost Pengejar)



| Komponen PEAS | Deskripsi Sistem |
| --- | --- |
| **Performance Measure**

 | Kemampuan menangkap Pac-Man, meminimalkan waktu pencarian (*search time*), meminimalkan jumlah simpul yang diperiksa (*nodes explored*), dan efisiensi panjang jalur.

 |
| **Environment**

 | Grid 2D statis/dinamis yang terdiri atas Jalur, Dinding, Pintu Keluar, Pac-Man, dan Hantu.

 |
| **Actuators**

 | Eksekusi pergerakan fisik Ghost ke Atas, Bawah, Kiri, atau Kanan sepanjang grid.

 |
| **Sensors**

 | Pembacaan koordinat posisi Pac-Man, koordinat posisi Ghost, dan peta matriks dinding/jalur.

 |

---

## 5. Algoritma Pathfinding & Logika Pencarian

### A. Uninformed Search: Breadth-First Search (BFS)



* **Prinsip Operasi:** Menelusuri ruang keadaan secara melapis (*level-by-level*) dari simpul awal.


* **Struktur Data:** Queue (FIFO - *First In First Out*).


* **Mekanisme:**
1. Masukkan posisi Ghost ke dalam Queue.


2. Ekstrak elemen terdepan, periksa 4 tetangga (Atas, Bawah, Kiri, Kanan) yang valid.


3. Tandai node terhitung untuk menghindari *loop*, catat *parent node*.


4. Hentikan saat posisi Pac-Man ditemukan.




* **Sifat Optimalitas:** Menjamin jalur terpendek dalam hal jumlah langkah pada grid dengan *cost* seragam.



### B. Informed Search: Algoritma $A^*$ (A-Star)



* **Prinsip Operasi:** Memprioritaskan penelusuran simpul berdasarkan fungsi evaluasi biaya terendah:



$$f(n) = g(n) + h(n)$$





* $g(n)$: Biaya aktual yang ditempuh dari posisi Ghost ke simpul $n$ (jumlah langkah).


* $h(n)$: Perkiraan biaya heuristik dari simpul $n$ ke posisi Pac-Man.




* **Fungsi Heuristik (Manhattan Distance):**


$$h(n) = \vert{}x_n - x_t\vert{} + \vert{}y_n - y_t\vert{}$$



*(Sangat cocok karena pergerakan hanya 4 arah non-diagonal)*.


* **Struktur Data:** Priority Queue (Min-Heap berdasarkan nilai $f(n)$).



### C. Logika Dynamic Path Planning (Pencarian Ulang)



* Setiap kali Pac-Man berpindah 1 kotak grid, status target berubah.


* Agen AI Ghost memicu panggilan ulang (*re-pathfinding*) menggunakan posisi Ghost saat itu sebagai *start node* dan koordinat baru Pac-Man sebagai *goal node*.



---

## 6. Skenario & Parameter Pengujian Kinerja (Benchmark Metrics)

### Skenario Pengujian



1. **Skenario Pac-Man Diam (Static Target):**


* Pac-Man tetap di lokasi awal. Membandingkan performa pencarian murni BFS vs $A^*$ pada satu eksekusi rute tunggal di tiap maze.




2. **Skenario Pac-Man Bergerak (Dynamic Target):**


* Pemain menggerakkan Pac-Man. Urutan pergerakan Pac-Man disamakan pada kedua algoritma untuk menjamin objektivitas pengujian. Pencarian ulang dijalankan setiap kali Pac-Man melangkah.





### Parameter Pengukuran Kinerja



1. **Waktu Pencarian (Search Time / Execution Time):** Durasi waktu (milidetik) yang dibutuhkan algoritma untuk menyelesaikan komputasi jalur.


2. **Jumlah Simpul yang Diperiksa (Nodes Explored):** Total node/kotak grid yang dievaluasi/dikunjungi selama proses pencarian berlangsung.


3. **Panjang Jalur (Path Length):** Jumlah total langkah (*cost*) jalur solusi yang ditemukan.


4. **Game Result & Duration:** Hasil akhir (Menang/Kalah) serta total waktu hingga sesi permainan berakhir.



---

## 7. Plan of Execution (Jadwal Pengerjaan Proyek)

Proyek dilaksanakan selama 7 minggu (Minggu ke-9 hingga Minggu ke-15) dengan pembagian kerja sebagai berikut:

| No | Tahap Kegiatan Proyek | M9 | M10 | M11 | M12 | M13 | M14 | M15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Studi Literatur & Penyusunan Proposal

 | X | X |  |  |  |  |  |
| 2 | Perancangan Maze & Mekanisme Permainan

 |  | X | X |  |  |  |  |
| 3 | Implementasi Pergerakan Pac-Man & Ghost

 |  |  | X | X |  |  |  |
| 4 | Implementasi Algoritma BFS & $A^*$

 |  |  |  | X | X |  |  |
| 5 | Pengujian pada 3 Maze & 2 Kondisi Targets

 |  |  |  |  | X | X |  |
| 6 | Analisis Hasil Pengujian & Refactoring Code

 |  |  |  |  |  | X | X |
| 7 | Penyusunan Laporan Akhir & Finalization

 |  |  |  |  |  |  | X |

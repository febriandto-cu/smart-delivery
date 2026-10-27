# Smart Delivery & Order Optimization System

Kelompok 1 — Data Structure and Algorithm, Semester 5, 2026/2027.
Fondasi kerja tim UAS berdasarkan [Guideline UAS](Materi/Guideline_UAS_Data_Structure_and_Algorithm.pdf)
dan [naskah UTS](<Materi/Naskah Presentasi Final — Kelompok 1.pdf>).

**Mulai dari [rencana dan pembagian UAS](docs/UAS_PLAN.md).** Cakupan UAS adalah
12 sesi (1–7, 9–13). Fondasi UTS sudah berjalan: Min/MaxHeap, dispatcher dasar,
Hash Table chaining, Trie, AVL, dan Held-Karp tabulation. Perluasan UAS seperti
aging, probing, RB/B-Tree, memoization, DP lanjut dan algoritma graf masih
memerlukan implementasi. Proyek ini belum menyelesaikan semua sesi UAS.

## Menjalankan di Windows PowerShell

Python 3.10+ diperlukan. Dari root proyek:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Buka `http://localhost:8501`. Perintah langsung ke virtual environment tidak
memerlukan aktivasi PowerShell. Di macOS/Linux gunakan `.venv/bin/python`.

Aplikasi langsung membuka **Order Management**; halaman beranda “app” disembunyikan.
**UAS Workspace** dan **Bagian Individu** juga disembunyikan dari sidebar dan
tautan pada halaman fitur. File serta URL internalnya tetap tersedia.
Menu **UAS Workspace** menampilkan kartu sembilan anggota. Klik **Buka bagian saya** atau
buka menu **Bagian Individu**, lalu pilih nama. Tersedia tiga tab:

- **Tugas & alur presentasi:** materi yang disiapkan dan urutan demonstrasi.
- **Demo bagian saya:** output kode asli, termasuk simulasi MaxHeap mandiri,
  bucket Hash, pencarian Trie, empat rotasi AVL, DP vs brute force, dan tes.
- **File & bukti:** file terkait dan artefak presentasi yang perlu dikumpulkan.

Atika mendapat ringkasan pembukaan/penutup, Husnu arsitektur, Eka pemetaan fitur,
lima pemateri teknis mendapat modul masing-masing, Daffa tes/eksperimen.
Menu **UAS Workspace** tetap menyimpan cakupan 12 sesi, target level dan audit
bukti. Status file/smoke test tidak berarti seluruh rubrik UAS terpenuhi.

Menu **Evidence & Dataset** menyediakan lima tab untuk anggota/dosen: dataset
beserta distribusi prioritas/status, delapan pemeriksaan algoritma dengan
input–expected–actual, riwayat aksi demo, benchmark/log tes dari session, dan
paket ZIP. Pilih sumber **Dataset aplikasi** atau **Demo presentasi**. Tanpa aksi
demo, halaman menampilkan contoh awal dengan label eksplisit. CSV sumber tidak
menyimpan seed; aplikasi mencatatnya sebagai tidak diketahui, disertai checksum
file sumber agar asal data tetap bisa diverifikasi.

Paket ZIP mencakup CSV lengkap, metadata/seed/jumlah data, checksum SHA-256,
hasil delapan kasus dan trace, serta riwayat/benchmark/log yang sudah tersedia.
Klik **Siapkan paket bukti ZIP**, lalu **Unduh paket bukti ZIP**. Siapkan ulang
setelah data berubah. Bukti kasus memakai input kecil terpisah; bukan pengujian
seluruh UAS, dan tidak menggantikan screenshot nyata beserta interpretasinya.

### Demo Order Management

Halaman Order Management langsung membuka **Dataset aplikasi** dengan seluruh
order CSV. Untuk latihan singkat, pilih **Demo presentasi**: empat order
Andi, Budi, Citra, Dewi. Urutan awal **Citra → Dewi → Budi → Andi** dihitung
oleh MaxHeap asli. Kartu order berikutnya menjelaskan alasan pemilihan.

1. Klik **Proses order berikutnya** dan amati perpindahan urutan.
2. Tambahkan order baru atau pilih order pada **Batalkan order yang menunggu**.
3. Buka **Riwayat aksi** untuk membaca perubahan atau mengunduh CSV.
4. Klik **Mulai ulang demo** untuk kembali ke empat order awal.

Tab **Cara Max-Heap memilih** menjelaskan tiga aturan dan menyediakan pohon/array
di expander. Tab **Panduan pemateri** berisi contoh narasi Febri Anggoro dan
keterkaitan Hash Table Rigan. Status diproses belum berarti selesai diantar.

Mode **Dataset aplikasi** memakai data bersama dengan halaman Search
dan Delivery Route. Order dari mode demo terisolasi dan tidak muncul di Search.
Mode terakhir diingat saat berpindah halaman. Memulai ulang demo tidak mengubah
dataset bersama atau order operasional.

## Pilihan heap tim

Dispatcher menggunakan **Max-Heap**, sesuai preferensi tim dan mapping slide 7
PPT UTS. Skor: **Urgent=3, High=2, Normal=1**. Waktu lebih awal menang; sequence
menjaga FIFO ketika timestamp sama. Enum data lama tetap Urgent=1, High=2,
Normal=3; `Order.max_heap_key()` memetakan level ke skor (`4-level`).
MinHeap tetap menjadi pelengkap wajib S1 dan dapat dipakai Prim; bukan heap
dispatcher. Aging masih TODO. Detail koreksi slide dan batas klaim:
[keputusan Max-Heap](docs/MAX_HEAP_DECISION.md).

## Dataset

```powershell
.\.venv\Scripts\python.exe -m src.data.generator --orders 100000 --restaurants 10000 --menus 150000 --seed 42
```

Menghasilkan `data/orders.csv`, `data/restaurants.csv`, `data/menus.csv`.
Gunakan jumlah positif; CSV dengan nama sama ditimpa. Angka ini skala desain UTS,
bukan pengukuran industri. **Aplikasi langsung membaca seluruh baris** dari
`data/orders.csv`, `data/restaurants.csv`, dan `data/menus.csv`, tanpa sampling
atau pengganti acak. CSV lokal saat perubahan ini berisi 100.000 order, 10.000
restoran, dan 50.000 menu. Jumlah aktual selalu mengikuti isi file.

Menu **Evidence & Dataset** menyediakan **Muat ulang seluruh CSV**. CSV yang berubah dideteksi
melalui signature file dan dimuat ulang otomatis. Aksi tambah/proses/batal/rating
berlaku dalam session; file asli tidak ditimpa. Memuat ulang mengembalikan isi CSV
serta mengosongkan log aksi operasional. CSV yang tidak lengkap/invalid menghasilkan
pesan error, tidak diganti dataset sintetis secara diam-diam.

Evidence menampilkan seluruh tabel dan menyediakan CSV lengkap. Search dengan
prefix kosong menampilkan seluruh restoran/menu; prefix terisi menampilkan semua
kecocokan. Pilihan restoran, ranking default, dan tabel antrean juga tidak dipotong.
Tabel dapat digulir; semua baris tetap tersedia. Batas **15 customer per rute**
Held-Karp dan batas brute force tetap merupakan batas algoritma, bukan batas
pemuatan dataset. Jika restoran punya <=15 order aktif, semua dipilih otomatis;
untuk restoran yang lebih besar, pilih batch secara eksplisit.

Halaman Delivery Route memakai koordinat order/restoran dari CSV yang sama atau
peta sintetis yang dipilih khusus untuk eksperimen.
Metadata berat/deadline/zona/kapasitas untuk modul baru masih perlu ditambahkan
melalui adapter bersama, bukan dataset terpisah per halaman.

## Pembagian implementasi dan presentasi

| Anggota | Bagian presentasi sesuai tabel UTS |
| --- | --- |
| Atika | Pembukaan, tim, background, problem statement; timeline, kesimpulan, referensi |
| Husnu | Objectives, functional requirements, arsitektur |
| Eka | Pemetaan fitur ke struktur data |
| Febri Anggoro | Heap & Priority Queue |
| Rigan | Hash Table |
| Rendi | Trie |
| Febri Andri | AVL Tree |
| M Febri | Dynamic Programming |
| Daffa | Complexity, testing, eksperimen |

Peran presentasi mengikuti tabel yang dikonfirmasi pengguna; durasi UTS total
28 menit. Pemilik implementasi tambahan S6, S9–S13 dan reviewer belum ditentukan.
Kebutuhan UAS tetap tercatat, dengan alokasi terpisah dari peran presentasi.
Detail slide dan durasi: `src/uas.py`, UAS Workspace, dan
[rencana UAS](docs/UAS_PLAN.md).

## Struktur proyek

```text
app.py                  Navigasi; langsung membuka Order Management
src/home.py             Arsip beranda lama, tidak tampil pada navigasi
pages/                  5 fitur aplikasi + UAS Workspace + Bagian Individu
src/presentation.py     Tugas, alur demo, file dan bukti per pemateri
src/presentation_ui.py  Panduan per anggota dan demo interaktif mandiri
src/models.py           Order, Restaurant, MenuItem, Courier
src/ds/                 Min/MaxHeap, Hash, Trie, AVL dan kontrak probing/RB/B-Tree/UnionFind
src/algorithms/         DP rute, oracle brute force, kontrak DP lanjut/Greedy/MST/path/flow
src/services/           Wiring UI, benchmark, audit UAS dan kontrak PQ aging
src/uas.py              Satu peta sesi, bobot, pemilik, target, klaim dan eksperimen
src/data/               Loader CSV seluruh baris + generator sintetis dengan seed
tests/                  Tes awal UTS + tes pendukung UAS; tes modul baru dikerjakan pemilik
experiments/            Runner, petunjuk, output CSV dan metadata JSON
docs/UAS_PLAN.md        Gap UTS→UAS, kontribusi, integrasi dan alur presentasi
docs/REPORT_TEMPLATE.md Kerangka IMRAD, matriks klaim-bukti, kontribusi dan bantuan AI
docs/evidence/          Paket gambar/tabel/grafik/slide tiap sesi
Materi/                 PDF acuan asli tim
```

## Pengujian dan eksperimen

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pytest tests/test_uas_support.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_heap.py -q
.\.venv\Scripts\python.exe -m experiments.run --exp E1 --sizes 1000 10000 --repeats 5
```

Suite awal: 5 lulus, 35 gagal karena TODO. Setelah fondasi dan alur individu
dilengkapi, halaman order didesain ulang dan CSV digunakan penuh: **69 tes lulus**, termasuk UI tambah/cari/batal order dan pilihan
sembilan anggota. Tes tersebut belum mencakup algoritma perluasan yang masih
berupa kontrak. Jangan mengubah tes menjadi skip untuk menyembunyikan algoritma
yang belum jadi. Marker `opsional` berasal dari
UTS; change-priority/aging tetap termasuk target Level 2 S2 UAS.

Performance Lab/runner saat ini E1–E5. **Minimal lima pengulangan, median dan satu
warm-up**; pengukuran memori pada run terpisah. CSV mencatat sampel mentah, seed,
versi Python dan OS; CLI menambah metadata JSON. Tambahkan eksperimen sesi baru
bersama Daffa. Lihat [prosedur eksperimen](experiments/README.md).

Jangan mengutip angka speedup dari implementasi referensi sebagai hasil proyek.
Baseline yang dilewati karena batas bukan bukti timeout. Klaim teoretis perlu
validator, oracle dan bukti eksekusi; grafik pengukuran mendukung pertumbuhan,
bukan pembuktian formal Big-O dengan sendirinya.

## Aturan kerja

1. Inti ditulis manual. Library untuk UI/visualisasi/pengukuran/oracle boleh;
   tidak untuk menggantikan algoritma yang dinilai. Tidak memakai `heapq`,
   `hash()`, `dict` sebagai tabel hash, `bisect`, atau algoritma siap pakai di inti.
2. Pertahankan kontrak API lama. Tambahkan API/adapter untuk perluasan; perubahan
   model/service bersama direview Husnu. Docstring file baru adalah kontrak kerja,
   bukan implementasi selesai.
3. Satu branch/PR fokus satu bagian; review silang, tidak push langsung main.
   Setiap anggota menyimpan kontribusi faktual melalui commit, PR, tes dan bukti.
4. Definisi selesai: correctness+validator+integrasi+eksperimen+bukti+laporan+slide
   dan reviewer dapat menjalankan ulang. Minimal dua gambar dan satu tabel tiap
   sesi; grafik untuk minimal delapan sesi. S13 minimal lima kasus uji.
5. Semua anggota latihan QnA lintas modul. Nyatakan penggunaan AI/bantuan sesuai
   panduan. Jangan mengisi hasil atau kontribusi yang belum dilakukan.

PDF memuat konflik tanggal/durasi/halaman/slide. Rujukan halaman dan usulan
konservatif ada di [catatan panduan](docs/UAS_PLAN.md#ketentuan-pdf-yang-perlu-dikonfirmasi-ke-dosen).

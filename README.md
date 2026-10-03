# Smart Delivery & Order Optimization System

Group 1, Data Structure and Algorithm, Semester 5 (2026/2027).
Implementasi UAS dari proposal UTS: Min-Heap Priority Queue, Hash Table (Separate Chaining),
Trie, AVL Tree, dan Dynamic Programming Held-Karp, dengan antarmuka Streamlit.

## Menjalankan

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py             # aplikasi
pytest                           # semua test
pytest tests/test_heap.py        # test satu modul saja
pytest -m "not opsional"         # hanya test fitur wajib
python -m src.data.generator --orders 100000 --restaurants 10000 --menus 50000   # dataset CSV ke data/
```

Halaman Beranda menampilkan status setiap modul (Siap / Belum diimplementasi / Error).
Halaman yang modulnya belum selesai tetap terbuka dan menampilkan pesan, bukan crash.

## Struktur

```
app.py                      Beranda + status modul
pages/                      5 halaman Streamlit (Order, Search, Ranking, Delivery Route, Performance Lab)
src/models.py               Entitas Order, Restaurant, MenuItem, Courier (Proposal 7.2)
src/ds/                     heap.py, hash_table.py, trie.py, avl.py      <- TODO tim
src/algorithms/             dp_route.py (TODO tim), brute_force.py (sudah jadi)
src/services/               Service layer penghubung UI dan struktur data (sudah jadi)
src/baselines.py            Pendekatan naif untuk eksperimen (sudah jadi)
src/data/generator.py       Dataset sintetis dengan seed tetap (sudah jadi)
src/utils/timer.py          Alat ukur waktu dan memori (sudah jadi)
tests/                      TC-01 s.d. TC-18 sesuai Proposal Bagian 11
```

## Pembagian file

| Peran | File yang dikerjakan | Test yang harus lulus | Halaman |
| --- | --- | --- | --- |
| Heap & PQ Engineer | `src/ds/heap.py` | `tests/test_heap.py` | Order Management |
| Hash Table Engineer | `src/ds/hash_table.py` | `tests/test_hash_table.py` | Search (tab Order) |
| Trie Engineer | `src/ds/trie.py` | `tests/test_trie.py` | Search (tab Restoran, Menu) |
| AVL Tree Engineer | `src/ds/avl.py` | `tests/test_avl.py` | Ranking |
| DP Engineer | `src/algorithms/dp_route.py` | `tests/test_dp.py` | Delivery Route |
| QA & Performance Lead | `tests/`, `src/services/benchmark_service.py`, `src/baselines.py` | `tests/test_integration.py` | Performance Lab |
| System Architect | `src/ui.py`, `src/services/`, `app.py`, tampilan halaman | semua halaman tanpa error | semua |
| Business Analyst | validasi fitur vs Functional Requirements, teks UI, user flow | - | Order Management |
| Ketua | review PR, integrasi, laporan UAS | `pytest` hijau di `main` | Beranda |

Setiap fungsi yang harus dikerjakan berisi `raise NotImplementedError("TODO(...)")` beserta
docstring yang menjelaskan tugasnya dan target kompleksitasnya.

## Aturan main

1. **Jangan ubah kontrak** yang tertulis di docstring paling atas setiap file (nama method,
   parameter, bentuk return). Service, test, dan benchmark bergantung pada kontrak itu.
   Usulan perubahan dibahas dulu dengan ketua.
2. **Implementasi manual.** Dilarang memakai `heapq`, `dict` sebagai penyimpanan Hash Table,
   `hash()` bawaan, `bisect`, atau library struktur data lain di dalam `src/ds/` dan `dp_route.py`.
3. Nama fungsi sama dengan pseudocode di Proposal Bagian 8, supaya laporan UAS mudah
   merujuk ke proposal.

## Alur kerja Git

1. Ketua membuat repository GitHub (private) dari folder ini dan mengundang semua anggota.
2. Setiap anggota bekerja di branch sendiri: `feat/heap`, `feat/hash-table`, `feat/trie`,
   `feat/avl`, `feat/dp`, `feat/benchmark`, `feat/ui`.
3. Selesai satu bagian, buka Pull Request ke `main`. Buddy me-review, ketua yang merge.
4. Jangan push langsung ke `main`.

**Definisi selesai** untuk sebuah modul: semua test di file test-nya lulus, statusnya
"Siap" di Beranda, dan halamannya berfungsi.

## Catatan eksperimen (bahan QnA)

Baseline `SortedListPQ` memakai `bisect` yang ditulis dalam C, sedangkan Min-Heap kita
ditulis dalam Python murni. Akibatnya pada n kecil sorted list bisa lebih cepat. Uji coba
dengan implementasi referensi menunjukkan Min-Heap baru unggul mulai sekitar n = 50.000,
dan pada n = 100.000 sekitar 2,6x lebih cepat. Ini contoh nyata bahwa Big-O menggambarkan
pertumbuhan, bukan kecepatan absolut: konstanta bahasa dan implementasi ikut berpengaruh.
Jelaskan ini di laporan UAS dan siapkan jawabannya untuk sesi tanya jawab.

Baseline lain dilewati di atas batas tertentu (lihat `BASELINE_LIMIT`) karena terlalu lama.
Fakta bahwa baseline tidak sanggup selesai juga merupakan hasil eksperimen yang layak dilaporkan.

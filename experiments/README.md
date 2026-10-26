# Eksperimen UAS

Jalankan dari root proyek dengan virtual environment aktif:

```powershell
python -m experiments.run --exp E1 --sizes 1000 10000 50000 100000 --repeats 5
python -m experiments.run --exp E5 --sizes 4 6 8 --repeats 5
python -m pytest -q 2>&1 | Tee-Object -FilePath experiments/test-log.txt
```

CSV dan metadata JSON dibuat di `experiments/results/` dengan nama timestamp UTC.
`waktu_ms` adalah **median**, `samples_ms` berisi sampel mentah dalam JSON.
Satu warm-up tidak diukur. Run pengukuran peak memory terpisah agar tracemalloc
tidak mengubah sampel waktu. Minimal lima pengulangan, termasuk brute force.

E1/E4 mengukur pembangunan struktur + operasi. E2/E3 hanya mengukur query
pada indeks yang sudah dibangun; peak memory keduanya **bukan** total memori indeks.
Tambahkan eksperimen pembangunan/total indeks terpisah sebelum mengklaim hemat memori.
Semua pendekatan dalam satu perbandingan harus menyelesaikan pekerjaan ekuivalen.
E3 memakai `linear_prefix_groups` agar normalisasi, penggabungan ID nama sama,
urutan alfabet, dan batas jumlah kata sama seperti kontrak Trie. Tetap cross-check
hasil setelah Trie diimplementasi, termasuk input duplikat dan case-insensitive.

E1 kini **MaxHeap vs sorted list**, memakai `max_heap_key()` dan `extract_max()`
yang sama. Sorted list mengambil elemen terakhir dengan `pop()` O(1), bukan
`pop(0)` O(n); insert tetap O(n). Jangan memakai hasil E1 MinHeap lama untuk
mengklaim performa MaxHeap baru. Hasil historis tetap disimpan dengan labelnya.

Baris `belum diimplementasi` dan `dilewati` tidak boleh dimasukkan sebagai waktu 0.
Baseline yang dilewati berarti **tidak diukur karena kebijakan batas**, bukan bukti
bahwa baseline timeout atau kalah. Jangan menulis angka speedup sebelum eksekusi.
Hasil ini bukan pengukuran kecepatan aplikasi web atau database.

Rencana benchmark S1–S13 tersedia pada UAS Workspace dan `src/uas.py`.
Runner saat ini masih E1–E5; pemilik sesi menambahkan runner lain bersama Daffa.
Minimal delapan sesi membutuhkan grafik; satu grafik E1 tidak otomatis
memenuhi syarat dua sesi. Simpan raw CSV, lingkungan, tabel, dan interpretasi.

Perbarui RAM pada laporan. Tutup aplikasi berat, gunakan seed sama, catat ukuran,
parameter, batas baseline dan versi commit secara manual bersama hasil. Jangan
membandingkan run dari mesin berbeda tanpa menjelaskannya di Discussion.

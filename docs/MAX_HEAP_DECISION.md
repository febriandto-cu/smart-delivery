# Keputusan tim: dispatcher memakai Max-Heap

Sumber: [PPT UTS asli](<../Materi/UTS DSA Kelompok 1 — Smart Delivery & Order Optimization.pptx.pdf>).
Tim secara eksplisit memilih Max-Heap setelah memberikan PPT ini. PDF sumber
tetap sebagai arsip UTS. Pembagian pemateri tetap mengikuti tabel yang sudah
dikonfirmasi pengguna; tabel tanggung jawab slide 2 tidak mengganti pembagian itu.

## Kunci prioritas

| Prioritas | Level data lama | Skor Max-Heap |
| --- | --- | --- |
| Urgent | 1 | 3 |
| High | 2 | 2 |
| Normal | 3 | 1 |

Pemetaan `score = 4 - level` mempertahankan enum/data lama. MaxHeap memilih
tuple terbesar: `(score, -created_at, -sequence, order_id)`. Waktu lebih awal
mendapat nilai negatif lebih besar. Saat waktu sama, sequence enqueue yang
lebih kecil menang; order_id tidak menentukan FIFO. Contoh Urgent menit 10
mengalahkan Urgent menit 20; semua Urgent mengalahkan High/Normal.

`Order.max_heap_key()` menyediakan `(score, -created_at, order_id)`;
OrderPriorityQueue menambahkan sequence. `Order.heap_key()` tetap kompatibel
dengan MinHeap lama. Kontrak AgingPriorityQueue memakai effective_score dan
sequence pada waktu simulasi; aging belum diimplementasi. Created_at saat ini
masih menit dalam hari, sehingga urutan lintas hari perlu timestamp monotonik.

## Kode dan batas implementasi

- MaxHeap manual: insert, extract_max, peek, sift-up/down, build_heap,
  validator is_heap, trace swap opsional, update_priority, heap_sort.
- OrderPriorityQueue dan E1 memakai MaxHeap. HashTable chaining kini telah
  diimplementasikan; halaman order sudah dapat tambah, cari dan batalkan order.
- Update_priority mencari ID O(n), lalu memperbaiki heap O(log n); jangan
  mengklaim seluruh operasi O(log n) tanpa position map. Hasil update pada heap
  tidak otomatis mengubah objek Order; API service perubahan prioritas perlu
  menyinkronkan keduanya ketika diimplementasi.
- MinHeap juga telah diimplementasi sebagai pelengkap S1 dan dapat dipakai Prim.
- Trace swap adalah log proses, bukan pengganti visual pohon/screenshot UAS.
  Status smoke test MaxHeap lulus tidak berarti seluruh S1/S2 selesai.

## Penyelarasan materi UAS

| Slide UTS | Isi yang perlu diselaraskan pada materi UAS |
| --- | --- |
| 5–6 | Tujuan dan lapisan struktur: MaxHeap + PQ |
| 7 | Max-Heap sudah sesuai pilihan tim |
| 8 | Key skor dan waktu negatif; operasi extract_max |
| 9 | Urgent=skor 3, High=2, Normal=1; parent >= child; gambar pohon baru |
| 10 | Sift-up saat lebih besar; sift-down ke anak terbesar; extract_max |
| 19 | Nama MaxHeap/PQ dan extract_max; kompleksitas tetap |
| 20 | E1 MaxHeap vs sorted list; pakai hasil eksekusi baru |

Naskah presentasi bagian Heap juga perlu menggunakan istilah dan kunci yang sama.
Perubahan dari naskah MinHeap dijelaskan pada Discussion laporan; algoritma tetap
memenuhi tujuan bisnis mengambil order paling urgent lebih dahulu. Bukti nyata
dan angka benchmark dimasukkan setelah dijalankan, tanpa mengubah arsip PDF UTS.

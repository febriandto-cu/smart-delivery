# Kerangka laporan IMRAD dan kontribusi

Isi hanya dari kode/hasil nyata. Tanda `[isi]` adalah pekerjaan yang belum
dilakukan, bukan hasil penelitian. Rujukan ketentuan: Guideline hlm. 12–13,
catatan konflik minimal halaman di `UAS_PLAN.md`.

## Abstrak

[200–250 kata: masalah, metode, hasil angka yang sudah diuji, kesimpulan.]

Kata kunci: [4–6 kata kunci].

## I. Introduction

[Latar bisnis, asumsi 100.000 order / 10.000 restoran / 150.000 menu dari UTS
sebagai skala desain, bukan statistik industri. Problem dan objective terukur,
hubungan ke UTS, cakupan 12 sesi, perubahan desain dan alasan.]

## II. Methods

### Lingkungan dan dataset

[OS, CPU, RAM, Python, library, commit, generator, seed, distribusi, satuan,
ukuran, metadata order/kurir/graf, pengulangan ≥5, median, warm-up, metrik,
definisi setup dan batas baseline. Jelaskan arsitektur serta alur data.]

### Pola subbab S01–S07 dan S09–S13 (ulang 12 kali)

1. Desain, representasi, diagram, key dan invarian.
2. Pseudocode inti dan operasi khas.
3. Dasar teori dan kompleksitas waktu/ruang, best/average/worst bila berbeda.
4. Fitur bisnis, alasan pilihan dan alternatif.
5. Prosedur tes, input/expected, validator, oracle, edge case.
6. Prosedur eksperimen yang dapat direproduksi.

## III. Results

[Satu subbab setiap sesi: tabel input/expected/actual/status, output validator,
dua gambar minimal, tabel hasil, grafik minimal delapan sesi, interpretasi
sesudah setiap gambar/tabel. Tambah hasil alur integrasi lintas modul.]

| Sesi | Klaim | Input/seed | Tes/log | Gambar struktur | Screenshot | Tabel/grafik | Interpretasi | Slide |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Sxx] | [isi] | [isi] | [path] | [nomor] | [nomor] | [nomor] | [isi] | [A+B] |

## IV. Discussion

[Teori vs pertumbuhan pengukuran; konstanta Python, bias baseline C, kesetaraan
workload, memory setup yang dikecualikan, variasi mesin, batas ukuran, ancaman
validitas. Trade-off chaining/probing, AVL/RB/B-Tree, greedy/DP; alasan perubahan
UTS. Jangan mengasumsikan hasil waktu atau speedup yang belum diukur.]

## V. Conclusion

[Jawab objective memakai bukti, cakupan yang selesai, keterbatasan, pengembangan.]

## Referensi

[Minimal delapan sumber primer/buku/jurnal/dokumentasi resmi; gunakan APA atau
IEEE konsisten. Catat sumber yang benar-benar dibaca, bukan daftar contoh.]

## Lampiran

[Tautan repository, log pengujian, raw CSV, metadata mesin, materi demo cadangan.]

| Anggota | File/PR/commit yang dikerjakan | Tes/eksperimen | Gambar/tabel dan subbab | Reviewer |
| --- | --- | --- | --- | --- |
| [nama] | [kontribusi faktual] | [path] | [nomor] | [nama] |

Pernyataan bantuan: [sebut alat/AI, tujuan pemakaian, bagian yang dibantu,
validasi dan perubahan manual yang benar-benar dilakukan]. Seluruh anggota
tetap harus dapat menjelaskan dan memodifikasi kode saat defense.

# Paket bukti setiap sesi

Buat direktori `S01`, `S02`, …, `S07`, `S09`, …, `S13`, masing-masing berisi:

```text
Sxx/
  visual/           diagram struktur/proses dengan input pemicu
  screenshot/       screenshot eksekusi nyata, input-output terbaca
  table/            tabel kasus uji atau hasil, CSV sumbernya disertakan
  benchmark/        grafik berlabel dan raw CSV/metadata dari experiments/
  slides/           Slide A Klaim+Desain dan Slide B Bukti
  interpretation/   uraian hasil, batas klaim, rujukan Gambar/Tabel laporan
```

Minimal dua gambar dan satu tabel **per sesi**; grafik benchmark untuk minimal
delapan sesi. S13 minimal lima test case, sesi lain minimal satu (tetap uji setiap
operasi dan edge case). Memiliki satu file tes tidak berarti satu test case lulus.
Dashboard menghitung file nonkosong, bukan menilai autentisitas atau kelengkapan.
Jangan mengisi placeholder agar angka checklist terlihat penuh.

Simpan screenshot tanpa mock-up hasil. Satu diagram desain tidak menggantikan
screenshot nyata. Nomor dan angka PPT harus sama dengan laporan dan raw CSV.
Caption contoh: “Gambar 3.5 Rotasi LR setelah insert 30, 10, 20; root akhir 20.”
Setiap gambar diikuti interpretasi tentang kaitannya dengan klaim dan invarian.

Pemilik menandatangani cek, reviewer menjalankan ulang input yang sama, lalu
Atika menyelaraskan matriks klaim-bukti. Kelulusan sesi tidak diputus otomatis
oleh dashboard atau hanya berdasarkan smoke test pada Beranda.

"""Panduan individu sesuai pembagian pemateri yang disepakati pengguna.

Bagian presentasi bukan pengakuan kepengarangan kode. Kontribusi aktual tetap
dicatat melalui commit, tes, bukti, dan pemahaman anggota.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class MemberGuide:
    name: str
    role: str
    outcome: str
    files: tuple[str, ...]
    tasks: tuple[str, ...]
    demo_steps: tuple[str, ...]
    evidence: tuple[str, ...]
    page: str


GUIDES = (
    MemberGuide("Atika", "Pembukaan & penutup",
        "Menjelaskan masalah, konteks tim, hasil yang terbukti, serta keterbatasan sistem.",
        ("docs/UAS_PLAN.md", "docs/REPORT_TEMPLATE.md", "README.md"),
        ("Siapkan pembukaan: lima masalah bisnis dan tujuan aplikasi.",
         "Susun timeline, kesimpulan dan referensi berdasarkan hasil aktual.",
         "Pastikan rekap klaim dan kontribusi anggota sesuai bukti yang dikumpulkan."),
        ("Tampilkan ringkasan dataset dan alur aplikasi di bawah.",
         "Serahkan tujuan dan arsitektur kepada Husnu.",
         "Pada penutup, tampilkan hasil tes/eksperimen Daffa dan sebut bagian UAS yang belum selesai."),
        ("Naskah pembukaan dan penutup", "Rekap hasil dan keterbatasan", "Referensi serta kontribusi faktual"),
        "app.py"),
    MemberGuide("Husnu", "Tujuan, requirements & arsitektur",
        "Menunjukkan bagaimana kebutuhan bisnis mengalir dari UI ke service, algoritma, dan data.",
        ("src/models.py", "src/ui.py", "src/services/order_service.py", "src/services/delivery_service.py"),
        ("Petakan requirement UTS ke fitur yang sudah dapat dijalankan.",
         "Jelaskan empat lapisan dan tanggung jawab tiap service.",
         "Telusuri satu order: penyimpanan ID, antrean prioritas, status, lalu input rute."),
        ("Tampilkan diagram empat lapisan di bawah.", "Buka Order Management, pilih Dataset aplikasi, lalu tambah satu order.",
         "Cari ID tersebut pada Search, lalu jelaskan bahwa pemilihan batch rute belum otomatis dispatch."),
        ("Diagram arsitektur", "Tabel requirement dan fitur", "Screenshot alur data lintas halaman"),
        "pages/1_Order_Management.py"),
    MemberGuide("Eka", "Pemetaan fitur ke struktur data",
        "Menjelaskan alasan setiap fitur menggunakan struktur data tertentu dan trade-off alternatifnya.",
        ("src/uas.py", "src/models.py", "docs/UAS_PLAN.md", "docs/MAX_HEAP_DECISION.md"),
        ("Susun tabel fitur, key, operasi, alasan pemilihan dan alternatif.",
         "Jelaskan Max-Heap untuk prioritas, Hash untuk ID, Trie untuk prefix, AVL untuk ranking, DP untuk rute.",
         "Pisahkan fondasi UTS yang berjalan dari perluasan UAS yang belum memiliki penanggung jawab."),
        ("Gunakan tabel pemetaan di bawah.", "Bandingkan pencarian ID persis dengan prefix nama.",
         "Serahkan pembuktian teknis tiap struktur kepada pemateri berikutnya."),
        ("Tabel pemetaan fitur", "Penjelasan key dan alternatif", "Catatan perubahan Min-Heap ke Max-Heap"),
        "pages/2_Search.py"),
    MemberGuide("Febri Anggoro", "Max-Heap & Priority Queue",
        "Membuktikan Urgent keluar dahulu dan waktu/sequence menjaga urutan pada prioritas sama.",
        ("src/ds/max_heap.py", "src/ds/heap.py", "tests/test_max_heap.py", "src/services/priority_service.py"),
        ("Pelajari insert, sift-up, extract-max, sift-down, build-heap dan validator.",
         "Jelaskan skor Urgent=3, High=2, Normal=1 dan tie-break waktu/sequence.",
         "Lengkapi aging serta bukti S1–S2; demo dasar di bawah belum membuktikan anti-starvation."),
        ("Tambah order Normal, High dan Urgent pada simulasi di bawah.",
         "Amati root, array dan pohon; ambil order tertinggi.",
         "Uji dua Urgent dengan waktu sama untuk menunjukkan FIFO."),
        ("Pohon sebelum/sesudah operasi", "Trace dan hasil validator", "Benchmark build-heap dan PQ; bukti aging terpisah"),
        "pages/1_Order_Management.py"),
    MemberGuide("Rigan", "Hash Table",
        "Membuktikan ID ditemukan, collision ditangani, dan penghapusan tidak merusak key lain.",
        ("src/ds/hash_table.py", "tests/test_hash_table.py", "src/ds/open_addressing.py"),
        ("Jelaskan rolling hash, bucket chaining, put/get/remove dan rehash.",
         "Gunakan input collision dan perlihatkan load factor.",
         "Lengkapi open addressing/tombstone untuk target Level 2 UAS."),
        ("Cari ID pada tabel kecil di bawah dan amati bucket.", "Coba ID yang tidak ada.",
         "Buka Search untuk lookup ID dari dataset aplikasi."),
        ("Visual bucket collision", "Hasil lookup/delete/rehash", "Grafik probe/load factor; tombstone setelah diimplementasi"),
        "pages/2_Search.py"),
    MemberGuide("Rendi", "Trie",
        "Menunjukkan autocomplete dari prefix dengan normalisasi huruf dan batas hasil.",
        ("src/ds/trie.py", "src/services/search_service.py", "tests/test_trie.py"),
        ("Telusuri karakter, node terminal, item_ids dan DFS urut alfabet.",
         "Uji prefix ada/tidak ada, huruf besar dan nama sama pada dua ID.",
         "Lengkapi delete dan popularitas jika menargetkan level lanjut UAS."),
        ("Ketik ay, bakso atau prefix yang tidak ada di bawah.",
         "Bandingkan huruf besar dan kecil.", "Buka Search untuk restoran/menu pada dataset bersama."),
        ("Visual jalur prefix", "Screenshot autocomplete", "Benchmark vs linear scan dan jumlah node/memori"),
        "pages/2_Search.py"),
    MemberGuide("Febri Andri", "AVL Tree",
        "Membuktikan empat rotasi menjaga urutan BST, tinggi node, dan balance factor.",
        ("src/ds/avl.py", "src/services/ranking_service.py", "tests/test_avl.py"),
        ("Pelajari LL/RR/LR/RL, insert, delete/rebalance dan check_avl.",
         "Jelaskan composite key rating dan restaurant_id.",
         "Rekam empat kasus rotasi dan bandingkan tinggi AVL dengan BST terurut."),
        ("Pilih kasus rotasi di bawah; amati urutan insert dan root akhir.",
         "Tampilkan log serta validator.", "Buka Ranking untuk top-k dan pembaruan rating."),
        ("Empat visual before/after rotasi", "Log validator setelah operasi", "Tabel tinggi dan benchmark AVL vs BST"),
        "pages/3_Ranking.py"),
    MemberGuide("M Febri", "Dynamic Programming",
        "Membuktikan rute Held-Karp tanpa kembali ke restoran sama optimalnya dengan brute force.",
        ("src/algorithms/dp_route.py", "src/algorithms/dp_memo.py", "tests/test_dp.py", "src/services/delivery_service.py"),
        ("Jelaskan dp[mask][j], base case, transisi, parent dan rekonstruksi rute.",
         "Bandingkan biaya dengan brute force pada batch kecil.",
         "Lengkapi memoization untuk S7; DP lanjutan S9 masih belum dibagi."),
        ("Jalankan contoh restoran dan tiga customer di bawah.",
         "Bandingkan biaya DP dan brute force, lalu baca urutan antar.",
         "Buka Delivery Route untuk memilih order dari restoran yang sama."),
        ("State/recurrence dan tabel proses", "Hasil rekonstruksi serta oracle", "Eksperimen brute force/memo/tabulasi setelah memo selesai"),
        "pages/4_Delivery_Route.py"),
    MemberGuide("Daffa", "Complexity, testing & eksperimen",
        "Memastikan klaim tiap modul sesuai hasil pengujian, kompleksitas, dan pengukuran nyata.",
        ("tests/", "src/services/benchmark_service.py", "src/utils/timer.py", "experiments/run.py"),
        ("Jalankan tes dan periksa kasus normal, batas, oracle serta integrasi.",
         "Ukur minimal lima pengulangan, median, seed dan memori secara konsisten.",
         "Hubungkan raw CSV ke grafik/laporan; jelaskan batas baseline dan ruang lingkup tes."),
        ("Jalankan suite tes melalui tombol di bawah.", "Buka Performance Lab dan jalankan E1 ukuran kecil.",
         "Unduh CSV dan jelaskan hasil tanpa menganggap smoke test sebagai kelulusan seluruh UAS."),
        ("Log pengujian aktual", "Raw CSV dan metadata lingkungan", "Grafik, analisis Big-O dan keterbatasan"),
        "pages/5_Performance_Lab.py"),
)

FEATURE_MAPPING = (
    ("Antrean order", "Febri Anggoro", "Max-Heap + PQ", "(skor, -waktu, -sequence, ID)", "Urgent selalu didahulukan"),
    ("Cari ID order", "Rigan", "Hash Table", "order_id", "Lookup persis tanpa scan semua order"),
    ("Autocomplete", "Rendi", "Trie", "Karakter nama ternormalisasi", "Satu jalur per prefix"),
    ("Ranking restoran", "Febri Andri", "AVL Tree", "(rating, restaurant_id)", "Urutan dinamis dan top-k"),
    ("Rute satu batch", "M Febri", "Held-Karp DP", "(mask, titik terakhir)", "Submasalah rute dipakai ulang"),
)

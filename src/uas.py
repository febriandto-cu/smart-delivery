"""Peta kerja UAS. Status implementasi dihitung terpisah dari target rubrik.

Sumber: Materi/Guideline_UAS_Data_Structure_and_Algorithm.pdf halaman 4–15.
Pembagian presentasi mengikuti tabel UTS yang dikoreksi pengguna.
Pemilik sesi tambahan belum ditentukan; jangan menyamakan presenter dengan implementer.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionSpec:
    number: int
    title: str
    weight: int
    owner: str
    collaborators: str
    reviewer: str
    files: tuple[str, ...]
    tests: tuple[str, ...]
    feature: str
    minimum: str
    standard: str
    excellent: str
    claim: str
    experiment: str
    min_tests: int = 1

    @property
    def code(self) -> str:
        return f"S{self.number:02d}"


SESSIONS = (
    SessionSpec(1, "Heap", 4, "Febri Anggoro", "", "Belum ditentukan",
        ("src/ds/heap.py", "src/ds/max_heap.py"), ("tests/test_heap.py", "tests/test_max_heap.py"),
        "Priority Management",
        "MinHeap dan MaxHeap manual: insert, extract, peek, sift-up/down.",
        "build_heap O(n), heap sort, is_heap, dan trace heapify.",
        "Change-key/delete, gambar pohon, benchmark hingga 100.000 elemen.",
        "Heap property tetap benar setelah setiap operasi; build_heap bertumbuh linear.",
        "build_heap vs n kali insert; waktu, perbandingan, memori."),
    SessionSpec(2, "Priority Queue", 4, "Febri Anggoro", "", "Belum ditentukan",
        ("src/ds/heap.py", "src/services/priority_service.py"), ("tests/test_priority.py",),
        "Priority Management / Dispatch",
        "MaxHeap enqueue/dequeue/peek; skor Urgent=3, High=2, Normal=1; FIFO sequence.",
        "Aging, change-priority, trace minimal 50 kejadian masuk-keluar.",
        "Bandingkan heap vs list terurut/tak terurut; metrik waktu tunggu.",
        "Prioritas dan FIFO benar; aging mencegah order Normal tertinggal pada simulasi.",
        "PQ heap vs dua baseline; rata-rata/maksimum waktu tunggu."),
    SessionSpec(3, "Hash Table", 5, "Rigan", "", "Belum ditentukan",
        ("src/ds/hash_table.py", "src/ds/open_addressing.py"),
        ("tests/test_hash_table.py", "tests/test_open_addressing.py"), "Search Center",
        "Hash manual, separate chaining, insert/search/delete.",
        "Linear probing, tombstone, rehash, load factor, penghitung collision.",
        "Quadratic probing, double hashing; dua fungsi hash dan clustering.",
        "Collision dan delete benar; lookup rata-rata mendekati O(1) dengan load terkendali.",
        "Rata-rata probe vs load factor 0,3–0,9; chaining vs probing."),
    SessionSpec(4, "Trie", 5, "Rendi", "", "Belum ditentukan",
        ("src/ds/trie.py",), ("tests/test_trie.py",), "Search Center",
        "Insert, exact search, starts_with.",
        "Autocomplete, delete, normalisasi case-insensitive.",
        "Top-k berdasarkan popularitas, benchmark linear, node/memori, diskusi radix.",
        "Autocomplete benar dan biaya penelusuran bergantung pada prefix serta subtree hasil.",
        "Trie vs linear scan di lima ukuran; jumlah node dan peak memory."),
    SessionSpec(5, "AVL Tree", 6, "Febri Andri", "", "Belum ditentukan",
        ("src/ds/avl.py",), ("tests/test_avl.py",), "Ranking and Index",
        "Insert, search, inorder, rotasi LL/RR/LR/RL.",
        "Delete/rebalance, validator BST+tinggi+balance, log rotasi.",
        "Top-k/range, AVL vs BST input terurut, gambar empat rotasi.",
        "AVL menjaga |BF| <= 1, urutan BST, serta tinggi tersimpan yang benar.",
        "AVL vs BST terurut: tinggi, waktu, rotasi, node access."),
    SessionSpec(6, "Red-Black Tree dan B-Tree", 6, "Belum ditentukan", "", "Belum ditentukan",
        ("src/ds/rb_tree.py", "src/ds/b_tree.py"),
        ("tests/test_rb_tree.py", "tests/test_b_tree.py"), "Ranking and Index",
        "RB insert/recolor/rotasi/search; B-Tree insert/split/search.",
        "Validator seluruh invarian; delete pada sedikitnya satu struktur.",
        "AVL vs RB vs B-Tree: tinggi/rotasi/node access; beberapa degree t.",
        "Validator RB dan B-Tree lulus; trade-off indeks aktif dan riwayat terukur.",
        "Tiga pohon pada kunci yang sama; simulasi page read B-Tree."),
    SessionSpec(7, "DP Rute: Memoization dan Tabulation", 5, "M Febri", "", "Belum ditentukan",
        ("src/algorithms/dp_route.py", "src/algorithms/dp_memo.py"),
        ("tests/test_dp.py", "tests/test_dp_memo.py"), "Delivery Route",
        "Held-Karp top-down dan bottom-up; state, recurrence, base case eksplisit.",
        "Keduanya sama dengan brute force; rekonstruksi rute dan jumlah state/panggilan.",
        "Optimasi ruang yang sesuai dependensi state; grafik naif/memo/tabulasi.",
        "Memoization dan tabulation menghasilkan biaya rute optimal yang sama dengan oracle.",
        "Brute force vs memo vs tabulasi; batch kecil, waktu/state/memori."),
    SessionSpec(9, "DP Lanjut", 8, "Belum ditentukan", "", "Belum ditentukan",
        ("src/algorithms/knapsack.py", "src/algorithms/lcs.py", "src/algorithms/edit_distance.py"),
        ("tests/test_knapsack.py", "tests/test_lcs.py", "tests/test_edit_distance.py"),
        "Optimization / Fuzzy Search",
        "0/1 Knapsack, LCS, Edit Distance; tabel DP.",
        "Backtracking ketiganya; cross-check oracle input kecil.",
        "Knapsack terhubung dispatch; fuzzy Trie+edit distance; optimasi ruang satu masalah.",
        "Tiga DP memberi nilai optimum dan solusi yang dapat direkonstruksi.",
        "Skala n dan W terpisah; O(nW) pseudo-polynomial; greedy ratio counterexample."),
    SessionSpec(10, "Greedy", 6, "Belum ditentukan", "", "Belum ditentukan",
        ("src/algorithms/greedy.py",), ("tests/test_greedy.py",), "Dispatch Optimization",
        "Dispatch earliest-deadline-first dengan asumsi tujuan eksplisit.",
        "Bukti exchange argument; perbandingan minimal 100 instance acak kecil.",
        "Dua strategi; counterexample ratio greedy pada 0/1 Knapsack.",
        "EDD meminimalkan maximum lateness pada satu kurir dengan asumsi yang dinyatakan.",
        "EDD vs brute force semua urutan; 100 instance seed tetap; ratio vs DP."),
    SessionSpec(11, "Minimum Spanning Tree", 6, "Belum ditentukan", "", "Belum ditentukan",
        ("src/ds/union_find.py", "src/algorithms/mst.py"), ("tests/test_mst.py",),
        "Network and Routing",
        "Kruskal + Union-Find compression/rank; Prim + heap manual.",
        "V-1 edge, terhubung, tanpa siklus, bobot sama; gambar MST.",
        "Sparse/dense; minimum spanning forest; cut/cycle property.",
        "Kruskal dan Prim menghasilkan MST valid dengan bobot yang sama.",
        "Graf yang sama: sparse/dense, V bertambah, waktu dan edge visit."),
    SessionSpec(12, "Shortest Path", 7, "Belum ditentukan", "", "Belum ditentukan",
        ("src/algorithms/shortest_path.py",), ("tests/test_shortest_path.py",),
        "Network and Routing",
        "Bellman-Ford dan Floyd-Warshall manual, termasuk edge negatif.",
        "Deteksi siklus negatif, rekonstruksi jalur, cross-check kedua metode.",
        "Bandingkan Dijkstra hanya pada non-negatif; trace Floyd per k; benchmark.",
        "Jarak dan jalur benar; siklus negatif terdeteksi dan ditandai.",
        "O(VE) vs O(V^3); biaya promo terpisah dari menit perjalanan."),
    SessionSpec(13, "Network Flow", 8, "Belum ditentukan", "", "Belum ditentukan",
        ("src/algorithms/flow.py",), ("tests/test_flow.py",), "Courier Allocation",
        "Ford-Fulkerson DFS atau Edmonds-Karp BFS dengan residual graph.",
        "Validator kapasitas/conservation, trace augmenting path, min-cut.",
        "Bipartite assignment; DFS vs BFS; verifikasi max-flow = min-cut.",
        "Alokasi memenuhi kapasitas, konservasi aliran, dan max-flow sama dengan min-cut.",
        "Jaringan kurir-zona sama; augmentasi, waktu, max-flow/min-cut.", min_tests=5),
)

# Slide dan durasi adalah acuan UTS, bukan batas presentasi UAS yang sudah disetujui.
PRESENTATION = (
    ("Atika", "01–04", "Pembukaan, tim, background, problem statement", 3.5),
    ("Husnu", "05–06", "Objectives, functional requirements, arsitektur", 3.5),
    ("Eka", "07–08", "Pemetaan fitur ke struktur data", 2.5),
    ("Febri Anggoro", "09–10", "Heap & Priority Queue", 2.5),
    ("Rigan", "11–12", "Hash Table", 2.5),
    ("Rendi", "13–14", "Trie", 2.5),
    ("Febri Andri", "15–16", "AVL Tree", 2.5),
    ("M Febri", "17–18", "Dynamic Programming", 3.5),
    ("Daffa", "19–20", "Complexity, testing, eksperimen", 3.5),
    ("Atika", "21–22", "Timeline, kesimpulan, referensi", 1.5),
)
TEAM = tuple(
    (name, "; ".join(row[2] for row in PRESENTATION if row[0] == name))
    for name in dict.fromkeys(row[0] for row in PRESENTATION)
)

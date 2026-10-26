"""S9 — pemilik belum ditentukan. Levenshtein untuk fallback fuzzy search nama restoran.

Normalisasikan via src.ds.trie.normalize; biaya insert/delete/replace = 1.
O(mn) waktu/ruang. Match = 0, transposition bukan satu operasi.
Trie tetap jalur utama; fuzzy dipakai ketika prefix kosong hasilnya.
"""


def edit_distance(first: str, second: str) -> dict:
    """Return {distance: int, operations: list[dict], table: list[list[int]]}.

    operations merekonstruksi first ternormalisasi menjadi second, dengan
    indeks yang dijelaskan jelas. Sertakan baris/kolom kosong pada tabel DP.
    """
    raise NotImplementedError("TODO(S9 pemilik belum ditentukan): Edit Distance + backtracking")

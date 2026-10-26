"""S9 — pemilik belum ditentukan. Pemilihan order dalam kapasitas satu kurir.

weights/capacity berupa unit integer positif/nonnegatif (bukan float kg);
values nilai bisnis nonnegatif, bukan waktu. Setiap item dipilih paling sekali.
Return optimum, indeks terpilih, tabel; O(nW) waktu/ruang, pseudo-polynomial.
Sesudah pemilihan, order_id diteruskan ke dispatch dan DP rute.
"""


def knapsack(weights: list[int], values: list[float], capacity: int) -> dict:
    """Return {value: float, selected_indices: list[int], table: list[list]}.

    Input kosong -> nilai 0 dan indeks kosong. Tolak panjang berbeda,
    weight nonpositif, capacity negatif. Tie diputus konsisten/didokumentasi.
    """
    raise NotImplementedError("TODO(S9 pemilik belum ditentukan): 0/1 Knapsack + backtracking")

"""S6 — pemilik belum ditentukan. Indeks riwayat order memakai key (completed_at, order_id).

Minimum degree t >= 2; node non-root t-1..2t-1 key, internal k+1 child,
seluruh leaf sama depth. Insert/split/search manual. Catat splits/node_accesses.
Page read hanyalah simulasi node access, bukan pengukuran disk sebenarnya.
"""


class BTree:
    def __init__(self, t: int = 3):
        if t < 2:
            raise ValueError("Minimum degree t harus >= 2")
        self.t = t

    def insert(self, key, value) -> None:
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): B-Tree insert/split")

    def search(self, key):
        """Return value atau None; ukur node access, bukan hanya comparisons."""
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): B-Tree search")

    def range_query(self, low, high) -> list[tuple]:
        """Return pasangan (key, value) urut naik; kedua batas inklusif."""
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): history range")

    def validate(self) -> dict:
        """Return {valid: bool, errors: list[str], height: int}."""
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): B-Tree validator")

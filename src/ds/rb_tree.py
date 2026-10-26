"""S6 — pemilik belum ditentukan. Indeks order aktif; RB-Tree manual.

Key = order_id, value = Order. Sentinel NIL hitam. Validasi BST, root hitam,
NIL hitam, anak red harus black, black-height sama; validasi parent link juga.
Catat recolor, rotation_log, node_accesses. Delete menjadi target L2 tim;
kontrak search mengembalikan None jika key tidak ada.
"""


class RBTree:
    def insert(self, key, value) -> None:
        """Update existing key tanpa menambah size; O(log n)."""
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): RB insert/fixup")

    def search(self, key):
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): RB search")

    def delete(self, key) -> bool:
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): RB delete/fixup")

    def validate(self) -> dict:
        """Return {valid: bool, errors: list[str], black_height: int}."""
        raise NotImplementedError("TODO(S6 pemilik belum ditentukan): RB validator")

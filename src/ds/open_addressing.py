"""S3 — Rigan. Tabel slot manual; bukan dict/hash() Python.

API put/get/remove sama dengan HashTable chaining. None = slot belum pernah
terisi; TOMBSTONE = bekas terhapus. Search tidak boleh berhenti di tombstone.
capacity prima, rehash dinamis; ukur collisions/probes terpisah.
Linear wajib L2; quadratic/double untuk L3. Jangan ganti default chaining UTS.
"""


class OpenAddressingHashTable:
    def __init__(self, capacity: int = 11, max_load: float = 0.75,
                 strategy: str = "linear"):
        if strategy not in {"linear", "quadratic", "double"}:
            raise ValueError("strategi probing tidak dikenal")
        self.strategy = strategy
        self.capacity = capacity
        self.max_load = max_load

    def put(self, key: str, value) -> None:
        raise NotImplementedError("TODO(S3 Rigan): probing put/rehash")

    def get(self, key: str):
        """Return value atau None; batasi probe agar tidak infinite loop."""
        raise NotImplementedError("TODO(S3 Rigan): probing get")

    def remove(self, key: str) -> bool:
        raise NotImplementedError("TODO(S3 Rigan): tombstone remove")

    def stats(self) -> dict:
        """capacity, size, tombstones, load_factor, collisions, probes."""
        raise NotImplementedError("TODO(S3 Rigan): probing stats")

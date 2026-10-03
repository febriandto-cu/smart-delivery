"""Hash Table dengan Separate Chaining (Proposal Bagian 6.2 dan 8.2).

Pemilik : Hash Table Engineer
Buddy   : Heap & PQ Engineer
Test    : tests/test_hash_table.py (TC-05 s.d. TC-08)

Kontrak yang TIDAK boleh diubah:
- `self.buckets` adalah list of list berisi pasangan (key, value),
  panjangnya `self.capacity` yang selalu bilangan prima.
- `self.size` = jumlah pasangan key-value yang tersimpan.
- Setelah put, jika load_factor() > max_load, panggil rehash() ke
  next_prime(2 * capacity).
- Dilarang memakai dict Python sebagai penyimpanan dan dilarang `hash()` bawaan.
"""
from __future__ import annotations

from typing import Any, Optional


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def next_prime(n: int) -> int:
    while not is_prime(n):
        n += 1
    return n


class HashTable:
    BASE = 31  # basis rolling hash polinomial

    def __init__(self, capacity: int = 11, max_load: float = 0.75) -> None:
        self.capacity = next_prime(capacity)
        self.max_load = max_load
        self.buckets: list[list[tuple[str, Any]]] = [[] for _ in range(self.capacity)]
        self.size = 0
        self.comparisons = 0

    # ---------- sudah jadi ----------
    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def load_factor(self) -> float:
        return self.size / self.capacity

    def stats(self) -> dict:
        """Statistik untuk halaman Search (FR-08)."""
        lengths = [len(b) for b in self.buckets]
        return {
            "capacity": self.capacity,
            "size": self.size,
            "load_factor": round(self.load_factor(), 3),
            "longest_chain": max(lengths) if lengths else 0,
            "empty_buckets": lengths.count(0),
        }

    # ---------- TODO pemilik modul ----------
    def hash_function(self, key: str) -> int:
        """Rolling hash polinomial: sum(ord(c) * BASE^i) mod capacity."""
        raise NotImplementedError("TODO(Hash Owner): HashTable.hash_function")

    def put(self, key: str, value: Any) -> None:
        """Insert atau update. Cek load factor setelahnya (TC-05, TC-07)."""
        raise NotImplementedError("TODO(Hash Owner): HashTable.put")

    def get(self, key: str) -> Optional[Any]:
        """Return value, atau None jika key tidak ada. Rata-rata O(1)."""
        raise NotImplementedError("TODO(Hash Owner): HashTable.get")

    def remove(self, key: str) -> bool:
        """Hapus key. Return True jika berhasil, False jika tidak ada (TC-08)."""
        raise NotImplementedError("TODO(Hash Owner): HashTable.remove")

    def rehash(self) -> None:
        """Pindahkan semua pasangan ke tabel baru berukuran next_prime(2 * capacity)."""
        raise NotImplementedError("TODO(Hash Owner): HashTable.rehash")

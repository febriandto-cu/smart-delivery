"""Min-Heap & Priority Queue (Proposal Bagian 6.1 dan 8.1).

Pemilik : Heap & PQ Engineer
Buddy   : Hash Table Engineer
Test    : tests/test_heap.py (TC-01 s.d. TC-04)

Kontrak yang TIDAK boleh diubah (dipakai service & benchmark):
- Elemen heap adalah tuple kunci (priority_level, created_at, order_id).
- Data disimpan dalam list `self._data`; elemen terkecil selalu di indeks 0.
- Setiap perbandingan antar elemen lewat `self._less()` agar `self.comparisons`
  terhitung untuk Performance Lab.
- Dilarang memakai modul `heapq`.
"""
from __future__ import annotations

from typing import Iterable, Optional

HeapKey = tuple[int, float, str]


class MinHeap:
    def __init__(self) -> None:
        self._data: list[HeapKey] = []
        self.comparisons = 0

    # ---------- sudah jadi ----------
    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def _less(self, i: int, j: int) -> bool:
        self.comparisons += 1
        return self._data[i] < self._data[j]

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # ---------- TODO pemilik modul ----------
    def insert(self, key: HeapKey) -> None:
        """Tambahkan key di akhir list lalu panggil sift_up. Target O(log n)."""
        raise NotImplementedError("TODO(Heap Owner): MinHeap.insert")

    def sift_up(self, i: int) -> None:
        """Naikkan elemen di indeks i selama lebih kecil dari parent-nya."""
        raise NotImplementedError("TODO(Heap Owner): MinHeap.sift_up")

    def extract_min(self) -> Optional[HeapKey]:
        """Ambil dan hapus root. Heap kosong -> return None (TC-03). Target O(log n)."""
        raise NotImplementedError("TODO(Heap Owner): MinHeap.extract_min")

    def sift_down(self, i: int) -> None:
        """Turunkan elemen di indeks i ke anak terkecil sampai sifat heap terpenuhi."""
        raise NotImplementedError("TODO(Heap Owner): MinHeap.sift_down")

    def peek(self) -> Optional[HeapKey]:
        """Lihat root tanpa menghapus. Heap kosong -> None. Target O(1)."""
        raise NotImplementedError("TODO(Heap Owner): MinHeap.peek")

    def build_heap(self, keys: Iterable[HeapKey]) -> None:
        """Bangun heap dari banyak key sekaligus dengan heapify bottom-up, O(n)."""
        raise NotImplementedError("TODO(Heap Owner): MinHeap.build_heap")

    def update_priority(self, order_id: str, new_level: int) -> bool:
        """OPSIONAL (FR-05, TC-04). Ubah level order lalu sift_up/sift_down.

        Saran: simpan position map order_id -> indeks agar pencarian posisi
        tidak O(n). Return False jika order_id tidak ada.
        """
        raise NotImplementedError("TODO(Heap Owner): MinHeap.update_priority (opsional)")


class OrderPriorityQueue:
    """Priority Queue untuk Order. Sudah jadi: hanya membungkus MinHeap."""

    def __init__(self) -> None:
        self.heap = MinHeap()

    def __len__(self) -> int:
        return len(self.heap)

    def push(self, order) -> None:
        self.heap.insert(order.heap_key())

    def pop(self) -> Optional[str]:
        key = self.heap.extract_min()
        return key[2] if key else None

    def peek(self) -> Optional[str]:
        key = self.heap.peek()
        return key[2] if key else None

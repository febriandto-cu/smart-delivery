"""MinHeap pelengkap S1 dan Priority Queue berbasis MaxHeap pilihan tim.

Pemilik : Heap & PQ Engineer
Buddy   : Hash Table Engineer
Test    : tests/test_heap.py (TC-01 s.d. TC-04)

Kontrak MinHeap lama (bukan heap utama dispatcher):
- Elemen heap adalah tuple kunci (priority_level, created_at, order_id).
- Data disimpan dalam list `self._data`; elemen terkecil selalu di indeks 0.
- Setiap perbandingan antar elemen lewat `self._less()` agar `self.comparisons`
  terhitung untuk Performance Lab.
- Dilarang memakai modul `heapq`.
"""
from __future__ import annotations

from typing import Iterable, Optional

from src.ds.max_heap import MaxHeap

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

    # ---------- operasi inti ----------
    def insert(self, key: HeapKey) -> None:
        """Tambahkan key di akhir list lalu panggil sift_up. Target O(log n)."""
        self._data.append(key)
        self.sift_up(len(self._data) - 1)

    def sift_up(self, i: int) -> None:
        """Naikkan elemen di indeks i selama lebih kecil dari parent-nya."""
        while i > 0:
            parent = (i - 1) // 2
            if not self._less(i, parent):
                break
            self._swap(i, parent)
            i = parent

    def extract_min(self) -> Optional[HeapKey]:
        """Ambil dan hapus root. Heap kosong -> return None (TC-03). Target O(log n)."""
        if not self._data:
            return None
        root, last = self._data[0], self._data.pop()
        if self._data:
            self._data[0] = last
            self.sift_down(0)
        return root

    def sift_down(self, i: int) -> None:
        """Turunkan elemen di indeks i ke anak terkecil sampai sifat heap terpenuhi."""
        while 2 * i + 1 < len(self._data):
            child = 2 * i + 1
            right = child + 1
            if right < len(self._data) and self._less(right, child):
                child = right
            if not self._less(child, i):
                break
            self._swap(i, child)
            i = child

    def peek(self) -> Optional[HeapKey]:
        """Lihat root tanpa menghapus. Heap kosong -> None. Target O(1)."""
        return self._data[0] if self._data else None

    def build_heap(self, keys: Iterable[HeapKey]) -> None:
        """Bangun heap dari banyak key sekaligus dengan heapify bottom-up, O(n)."""
        self._data = list(keys)
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self.sift_down(i)

    def update_priority(self, order_id: str, new_level: int) -> bool:
        """OPSIONAL (FR-05, TC-04). Ubah level order lalu sift_up/sift_down.

        Saran: simpan position map order_id -> indeks agar pencarian posisi
        tidak O(n). Return False jika order_id tidak ada.
        """
        if new_level not in (1, 2, 3):
            raise ValueError("Level harus 1, 2, atau 3")
        for i, key in enumerate(self._data):
            if key[2] == order_id:
                self._data[i] = (int(new_level), key[1], key[2])
                if i and self._less(i, (i - 1) // 2):
                    self.sift_up(i)
                else:
                    self.sift_down(i)
                return True
        return False


class OrderPriorityQueue:
    """Dispatcher berbasis MaxHeap; waktu lebih awal, lalu sequence FIFO.

    Key = (skor prioritas, -created_at, -sequence, order_id). Sequence naik
    saat push agar ID tidak menentukan FIFO ketika timestamp sama.
    """

    def __init__(self) -> None:
        self.heap = MaxHeap()
        self._sequence = 0

    def __len__(self) -> int:
        return len(self.heap)

    def push(self, order) -> None:
        score, time_key, order_id = order.max_heap_key()
        self.heap.insert((score, time_key, -self._sequence, order_id))
        self._sequence += 1

    def pop(self) -> Optional[str]:
        key = self.heap.extract_max()
        return key[-1] if key else None

    def peek(self) -> Optional[str]:
        key = self.heap.peek()
        return key[-1] if key else None

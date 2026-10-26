"""Max-Heap manual untuk dispatcher; Febri Anggoro, S1–S2.

Kunci tuple dibandingkan leksikografis: nilai terbesar di root. Untuk order
gunakan (skor, -created_at, -sequence, order_id). Tidak menggunakan heapq.
MinHeap tetap terpisah untuk cakupan S1 dan kebutuhan Prim.
"""
from __future__ import annotations

from typing import Iterable


class MaxHeap:
    def __init__(self, trace: bool = False) -> None:
        self._data: list[tuple] = []
        self.comparisons = 0
        self.trace_enabled = trace
        self.trace: list[dict] = []

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def _greater(self, i: int, j: int) -> bool:
        self.comparisons += 1
        return self._data[i] > self._data[j]

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]
        if self.trace_enabled:
            self.trace.append({"operation": "swap", "first": i, "second": j})

    def insert(self, key: tuple) -> None:
        self._data.append(key)
        self.sift_up(len(self._data) - 1)

    def sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if not self._greater(i, parent):
                break
            self._swap(i, parent)
            i = parent

    def peek(self) -> tuple | None:
        return self._data[0] if self._data else None

    def extract_max(self) -> tuple | None:
        if not self._data:
            return None
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self.sift_down(0)
        return root

    def sift_down(self, i: int) -> None:
        while 2 * i + 1 < len(self._data):
            child = 2 * i + 1
            right = child + 1
            if right < len(self._data) and self._greater(right, child):
                child = right
            if not self._greater(child, i):
                break
            self._swap(i, child)
            i = child

    def build_heap(self, keys: Iterable[tuple]) -> None:
        """Salin input lalu heapify bottom-up, O(n)."""
        self._data = list(keys)
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self.sift_down(i)

    def is_heap(self) -> bool:
        """Validasi parent >= child di seluruh array, O(n)."""
        return all(not self._greater(i, (i - 1) // 2) for i in range(1, len(self._data)))

    def update_priority(self, order_id: str, new_level: int) -> bool:
        """Level bisnis 1=Urgent, 2=High, 3=Normal; skor = 4-level.

        Cari ID O(n), perbaikan heap O(log n). Bagian waktu/sequence tetap.
        Jangan mengklaim seluruh operasi O(log n) tanpa position map.
        """
        if new_level not in (1, 2, 3):
            raise ValueError("Level prioritas harus 1, 2, atau 3")
        for i, key in enumerate(self._data):
            if key[-1] == order_id:
                self._data[i] = (4 - int(new_level), *key[1:])
                if i > 0 and self._greater(i, (i - 1) // 2):
                    self.sift_up(i)
                else:
                    self.sift_down(i)
                return True
        return False


def heap_sort(keys: list) -> list:
    """Salinan urut naik via MaxHeap manual; O(n log n), input tidak berubah."""
    heap = MaxHeap()
    heap.build_heap(keys)
    out = [heap.extract_max() for _ in range(len(heap))]
    out.reverse()
    return out

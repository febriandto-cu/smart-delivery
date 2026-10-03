"""Pendekatan naif sebagai pembanding di Performance Lab (Proposal Bagian 12).

Pemilik: QA & Performance Lead. Sudah jadi.
"""
from __future__ import annotations

from bisect import insort
from typing import Any, Optional


class SortedListPQ:
    """Baseline E1: list terurut. insert O(n) (geser elemen), extract O(n) (pop(0))."""

    def __init__(self) -> None:
        self._data: list = []

    def __len__(self) -> int:
        return len(self._data)

    def insert(self, key) -> None:
        insort(self._data, key)

    def extract_min(self):
        return self._data.pop(0) if self._data else None


def linear_search(orders: list, order_id: str):
    """Baseline E2: cek satu per satu, O(n)."""
    for order in orders:
        if order.order_id == order_id:
            return order
    return None


def linear_prefix_search(words: list[str], prefix: str, limit: int = 10) -> list[str]:
    """Baseline E3: periksa semua kata dengan startswith, O(n * m)."""
    prefix = prefix.lower()
    out = [w for w in words if w.lower().startswith(prefix)]
    return sorted(out)[:limit]


class _Node:
    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key, value) -> None:
        self.key, self.value, self.left, self.right = key, value, None, None


class NaiveBST:
    """Baseline E4: BST tanpa balancing. Input terurut -> tinggi n, operasi O(n)."""

    def __init__(self) -> None:
        self.root: Optional[_Node] = None
        self.size = 0

    def insert(self, key, value: Any) -> None:
        new = _Node(key, value)
        self.size += 1
        if self.root is None:
            self.root = new
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = new
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = new
                    return
                node = node.right

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

    def top_k(self, k: int) -> list:
        out, stack, node = [], [], self.root
        while (stack or node) and len(out) < k:
            while node:
                stack.append(node)
                node = node.right
            node = stack.pop()
            out.append((node.key, node.value))
            node = node.left
        return out

    def height(self) -> int:
        if self.root is None:
            return 0
        best, stack = 0, [(self.root, 1)]
        while stack:
            node, h = stack.pop()
            best = max(best, h)
            for child in (node.left, node.right):
                if child:
                    stack.append((child, h + 1))
        return best

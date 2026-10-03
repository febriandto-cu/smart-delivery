"""AVL Tree untuk ranking restoran (Proposal Bagian 6.4 dan 8.4).

Pemilik : AVL Tree Engineer
Buddy   : Trie Engineer
Test    : tests/test_avl.py (TC-12 s.d. TC-15)

Kontrak yang TIDAK boleh diubah:
- Kunci = tuple (rating, restaurant_id); value = objek Restaurant.
- Setiap rotasi dicatat di `self.rotation_log` dengan format
  "LL", "RR", "LR", atau "RL" diikuti kunci node yang tidak seimbang,
  contoh: "RR @ (4.2, 'R001')". Log ini ditampilkan di halaman Ranking.
- top_k dan range_query mengembalikan list of (key, value), rating menurun.
"""
from __future__ import annotations

from typing import Any, Optional

Key = tuple[float, str]


class AVLNode:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key: Key, value: Any) -> None:
        self.key = key
        self.value = value
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1


class AVLTree:
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None
        self.size = 0
        self.comparisons = 0
        self.rotation_log: list[str] = []

    # ---------- sudah jadi ----------
    def __len__(self) -> int:
        return self.size

    @staticmethod
    def height(node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def inorder(self) -> list[Key]:
        """Kunci urut naik (iteratif, aman untuk pohon tinggi). Dipakai test."""
        out, stack, node = [], [], self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            out.append(node.key)
            node = node.right
        return out

    def is_balanced(self) -> bool:
        """Cek |balance factor| <= 1 di semua node. Dipakai test."""
        def check(node: Optional[AVLNode]) -> int:
            if node is None:
                return 0
            hl, hr = check(node.left), check(node.right)
            if hl < 0 or hr < 0 or abs(hl - hr) > 1:
                return -1
            return 1 + max(hl, hr)
        return check(self.root) >= 0

    # ---------- TODO pemilik modul ----------
    def get_balance(self, node: Optional[AVLNode]) -> int:
        """height(left) - height(right)."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.get_balance")

    def rotate_right(self, y: AVLNode) -> AVLNode:
        """Rotasi kanan (kasus LL). Update tinggi, return root subtree baru."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.rotate_right")

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """Rotasi kiri (kasus RR). Update tinggi, return root subtree baru."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.rotate_left")

    def insert(self, key: Key, value: Any) -> None:
        """Insert BST lalu seimbangkan dengan 4 kasus LL/RR/LR/RL. O(log n)."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.insert")

    def delete(self, key: Key) -> bool:
        """Hapus key lalu seimbangkan ulang. Return False jika tidak ada."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.delete")

    def search(self, key: Key) -> Optional[Any]:
        """Return value atau None. O(log n)."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.search")

    def top_k(self, k: int) -> list[tuple[Key, Any]]:
        """k restoran rating tertinggi via reverse in-order. O(log n + k)."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.top_k")

    def range_query(self, min_rating: float) -> list[tuple[Key, Any]]:
        """Semua restoran dengan rating >= min_rating, rating menurun."""
        raise NotImplementedError("TODO(AVL Owner): AVLTree.range_query")

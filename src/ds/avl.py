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

    # ---------- operasi inti ----------
    def get_balance(self, node: Optional[AVLNode]) -> int:
        """height(left) - height(right)."""
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y: AVLNode) -> AVLNode:
        """Rotasi kanan (kasus LL). Update tinggi, return root subtree baru."""
        x = y.left
        y.left, x.right = x.right, y
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """Rotasi kiri (kasus RR). Update tinggi, return root subtree baru."""
        y = x.right
        x.right, y.left = y.left, x
        self.update_height(x)
        self.update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1:
            if self.get_balance(node.left) < 0:
                self.rotation_log.append(f"LR @ {node.key}")
                node.left = self.rotate_left(node.left)
            else:
                self.rotation_log.append(f"LL @ {node.key}")
            return self.rotate_right(node)
        if balance < -1:
            if self.get_balance(node.right) > 0:
                self.rotation_log.append(f"RL @ {node.key}")
                node.right = self.rotate_right(node.right)
            else:
                self.rotation_log.append(f"RR @ {node.key}")
            return self.rotate_left(node)
        return node

    def insert(self, key: Key, value: Any) -> None:
        """Insert BST lalu seimbangkan dengan 4 kasus LL/RR/LR/RL. O(log n)."""
        def add(node):
            if node is None:
                self.size += 1
                return AVLNode(key, value)
            self.comparisons += 1
            if key == node.key:
                node.value = value
                return node
            if key < node.key:
                node.left = add(node.left)
            else:
                node.right = add(node.right)
            return self._rebalance(node)
        self.root = add(self.root)

    def delete(self, key: Key) -> bool:
        """Hapus key lalu seimbangkan ulang. Return False jika tidak ada."""
        removed = False
        def remove(node, target):
            nonlocal removed
            if node is None:
                return None
            self.comparisons += 1
            if target < node.key:
                node.left = remove(node.left, target)
            elif target > node.key:
                node.right = remove(node.right, target)
            else:
                removed = True
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left:
                    successor = successor.left
                node.key, node.value = successor.key, successor.value
                node.right = remove(node.right, successor.key)
            return self._rebalance(node)
        self.root = remove(self.root, key)
        if removed:
            self.size -= 1
        return removed

    def search(self, key: Key) -> Optional[Any]:
        """Return value atau None. O(log n)."""
        node = self.root
        while node:
            self.comparisons += 1
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

    def top_k(self, k: int) -> list[tuple[Key, Any]]:
        """k restoran rating tertinggi via reverse in-order. O(log n + k)."""
        out, stack, node = [], [], self.root
        while (stack or node) and len(out) < k:
            while node:
                stack.append(node)
                node = node.right
            node = stack.pop()
            out.append((node.key, node.value))
            node = node.left
        return out

    def range_query(self, min_rating: float) -> list[tuple[Key, Any]]:
        """Semua restoran dengan rating >= min_rating, rating menurun."""
        out = []
        def collect(node):
            if node is None:
                return
            collect(node.right)
            if node.key[0] >= min_rating:
                out.append((node.key, node.value))
                collect(node.left)
        collect(self.root)
        return out

    def check_avl(self) -> bool:
        """Valideer BST, stored height, balance dan jumlah node; O(n)."""
        def check(node, low=None, high=None):
            if node is None:
                return 0, 0, True
            lh, lc, lv = check(node.left, low, node.key)
            rh, rc, rv = check(node.right, node.key, high)
            height = 1 + max(lh, rh)
            valid = (lv and rv and abs(lh - rh) <= 1 and node.height == height
                     and (low is None or low < node.key) and (high is None or node.key < high))
            return height, lc + rc + 1, valid
        _, count, valid = check(self.root)
        return valid and count == self.size

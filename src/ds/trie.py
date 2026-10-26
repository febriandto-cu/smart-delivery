"""Trie untuk prefix search restoran dan menu (Proposal Bagian 6.3 dan 8.3).

Pemilik : Trie Engineer
Buddy   : AVL Tree Engineer
Test    : tests/test_trie.py (TC-09 s.d. TC-11)

Kontrak yang TIDAK boleh diubah:
- Semua kata dinormalisasi lewat `normalize()` sebelum disimpan atau dicari.
- Node akhir kata menyimpan `item_ids` (restaurant_id atau menu_id).
- `starts_with` mengembalikan list of (kata, item_ids), maksimal `limit` kata,
  urut alfabetis.
"""
from __future__ import annotations


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


class TrieNode:
    __slots__ = ("children", "is_end", "item_ids")

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False
        self.item_ids: list[str] = []


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        self.word_count = 0
        self.node_count = 1  # untuk analisis memori di Performance Lab

    # ---------- operasi inti ----------
    def insert(self, word: str, item_id: str) -> None:
        """Telusuri/buat node per karakter, tandai is_end, tambahkan item_id. O(m)."""
        node = self.root
        for char in normalize(word):
            if char not in node.children:
                node.children[char] = TrieNode()
                self.node_count += 1
            node = node.children[char]
        if not node.is_end:
            node.is_end = True
            self.word_count += 1
        if item_id not in node.item_ids:
            node.item_ids.append(item_id)

    def search(self, word: str) -> bool:
        """True jika kata lengkap ada di Trie. O(m)."""
        node = self.root
        for char in normalize(word):
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix: str, limit: int = 10) -> list[tuple[str, list[str]]]:
        """O(m + node subtree yang dikunjungi + panjang output), termasuk urutan anak."""
        if limit <= 0:
            return []
        prefix = normalize(prefix)
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        out = []
        self.collect_words(node, prefix, out, limit)
        return out

    def collect_words(
        self, node: TrieNode, prefix: str, out: list[tuple[str, list[str]]], limit: int
    ) -> None:
        """DFS dari node, telusuri children urut alfabetis, berhenti saat out penuh."""
        # Iteratif: input nama panjang tidak menghabiskan recursion stack.
        stack = [(node, prefix)]
        while stack and len(out) < limit:
            current, word = stack.pop()
            if current.is_end:
                out.append((word, current.item_ids.copy()))
            # Insertion sort karakter manual; traversal inti tanpa sorted().
            chars = list(current.children)
            for i in range(1, len(chars)):
                char, j = chars[i], i - 1
                while j >= 0 and chars[j] > char:
                    chars[j + 1] = chars[j]
                    j -= 1
                chars[j + 1] = char
            for char in reversed(chars):
                stack.append((current.children[char], word + char))

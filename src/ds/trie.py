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

    # ---------- TODO pemilik modul ----------
    def insert(self, word: str, item_id: str) -> None:
        """Telusuri/buat node per karakter, tandai is_end, tambahkan item_id. O(m)."""
        raise NotImplementedError("TODO(Trie Owner): Trie.insert")

    def search(self, word: str) -> bool:
        """True jika kata lengkap ada di Trie. O(m)."""
        raise NotImplementedError("TODO(Trie Owner): Trie.search")

    def starts_with(self, prefix: str, limit: int = 10) -> list[tuple[str, list[str]]]:
        """Cari node prefix, lalu kumpulkan kata dengan collect_words. O(m + k)."""
        raise NotImplementedError("TODO(Trie Owner): Trie.starts_with")

    def collect_words(
        self, node: TrieNode, prefix: str, out: list[tuple[str, list[str]]], limit: int
    ) -> None:
        """DFS dari node, telusuri children urut alfabetis, berhenti saat out penuh."""
        raise NotImplementedError("TODO(Trie Owner): Trie.collect_words")

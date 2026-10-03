"""SearchService: Trie untuk restoran dan menu (Proposal Bagian 7.3, langkah 6).

Pemilik: System Architect (wiring). Sudah jadi; berfungsi setelah trie.py selesai.
"""
from __future__ import annotations

from src.ds.trie import Trie
from src.models import MenuItem, Restaurant


class SearchService:
    def __init__(self) -> None:
        self.restaurant_trie = Trie()
        self.menu_trie = Trie()
        # dict di bawah hanya untuk menampilkan detail hasil di UI,
        # bukan struktur data yang dinilai.
        self._restaurants: dict[str, Restaurant] = {}
        self._menus: dict[str, MenuItem] = {}

    def load(self, restaurants: list[Restaurant], menus: list[MenuItem]) -> None:
        for r in restaurants:
            self._restaurants[r.restaurant_id] = r
            self.restaurant_trie.insert(r.name, r.restaurant_id)
        for m in menus:
            self._menus[m.menu_id] = m
            self.menu_trie.insert(m.name, m.menu_id)

    def suggest_restaurants(self, prefix: str, limit: int = 10) -> list[Restaurant]:
        out = []
        for _, ids in self.restaurant_trie.starts_with(prefix, limit):
            out.extend(self._restaurants[i] for i in ids)
        return out[:limit]

    def suggest_menus(self, prefix: str, limit: int = 10) -> list[MenuItem]:
        out = []
        for _, ids in self.menu_trie.starts_with(prefix, limit):
            out.extend(self._menus[i] for i in ids)
        return out[:limit]

"""RankingService: AVL Tree (Proposal Bagian 7.3, langkah 6).

Pemilik: System Architect (wiring). Sudah jadi; berfungsi setelah avl.py selesai.
"""
from __future__ import annotations

from src.ds.avl import AVLTree
from src.models import Restaurant


class RankingService:
    def __init__(self) -> None:
        self.tree = AVLTree()

    def load(self, restaurants: list[Restaurant]) -> None:
        for r in restaurants:
            self.tree.insert(r.ranking_key(), r)

    def top(self, k: int = 10) -> list[Restaurant]:
        return [value for _, value in self.tree.top_k(k)]

    def above(self, min_rating: float) -> list[Restaurant]:
        return [value for _, value in self.tree.range_query(min_rating)]

    def update_rating(self, restaurant: Restaurant, new_rating: float) -> None:
        """Kunci berubah, jadi delete lalu reinsert (FR-13)."""
        self.tree.delete(restaurant.ranking_key())
        restaurant.rating = new_rating
        self.tree.insert(restaurant.ranking_key(), restaurant)

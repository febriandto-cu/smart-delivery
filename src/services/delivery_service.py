"""DeliveryService: DP Held-Karp vs brute force (Proposal Bagian 7.3, langkah 4-5).

Pemilik: System Architect (wiring). Sudah jadi; berfungsi setelah dp_route.py selesai.
"""
from __future__ import annotations

import time

from src.algorithms.brute_force import brute_force_route
from src.algorithms.dp_route import held_karp
from src.data.generator import generate_distance_matrix

BRUTE_FORCE_LIMIT = 9  # di atas ini brute force terlalu lama untuk demo


class DeliveryService:
    def make_matrix(self, n_customers: int, seed: int = 42) -> list[list[float]]:
        return generate_distance_matrix(n_customers, seed)

    def optimize(self, dist: list[list[float]]) -> dict:
        start = time.perf_counter()
        cost, route = held_karp(dist)
        return {"cost": cost, "route": route, "ms": (time.perf_counter() - start) * 1000}

    def brute_force(self, dist: list[list[float]]) -> dict | None:
        if len(dist) - 1 > BRUTE_FORCE_LIMIT:
            return None
        start = time.perf_counter()
        cost, route = brute_force_route(dist)
        return {"cost": cost, "route": route, "ms": (time.perf_counter() - start) * 1000}

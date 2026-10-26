"""DeliveryService: DP Held-Karp vs brute force (Proposal Bagian 7.3, langkah 4-5).

Pemilik: System Architect (wiring). Sudah jadi; berfungsi setelah dp_route.py selesai.
"""
from __future__ import annotations

import time
import math

from src.algorithms.brute_force import brute_force_route
from src.algorithms.dp_route import held_karp
from src.data.generator import generate_distance_matrix
from src.models import Order, Restaurant

BRUTE_FORCE_LIMIT = 9  # di atas ini brute force terlalu lama untuk demo


class DeliveryService:
    def matrix_for_orders(self, restaurant: Restaurant, orders: list[Order],
                          speed_kmh: float = 20.0) -> list[list[float]]:
        """Gunakan koordinat dataset bersama; titik 1..n sesuai urutan input.

        Ini model waktu Euclidean dengan kecepatan tetap, bukan rute jalan nyata.
        Promo negatif tidak boleh dimasukkan ke matriks waktu ini.
        """
        if not math.isfinite(speed_kmh) or speed_kmh <= 0:
            raise ValueError("Kecepatan harus positif dan finite")
        if len(orders) > 15:
            raise ValueError("Satu batch maksimal 15 customer")
        if len({o.order_id for o in orders}) != len(orders):
            raise ValueError("Order dalam batch tidak boleh duplikat")
        if any(o.restaurant_id != restaurant.restaurant_id for o in orders):
            raise ValueError("Satu batch harus berasal dari restoran yang sama")
        points = [restaurant.location, *(o.delivery_location for o in orders)]
        return [[round(math.dist(a, b) * 60.0 / speed_kmh, 3) for b in points] for a in points]

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

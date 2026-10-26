"""Delivery Optimization dengan DP Held-Karp (Proposal Bagian 9).

Pemilik : Dynamic Programming Engineer
Buddy   : QA & Performance Lead
Test    : tests/test_dp.py (TC-16, TC-17)

Kontrak:
- `dist` adalah matriks waktu tempuh (menit) berukuran (n+1) x (n+1).
  Titik 0 = restoran, titik 1..n = customer. Kurir TIDAK kembali ke restoran.
- Return (total_waktu_minimum, rute) dengan rute diawali 0 dan memuat
  semua titik tepat sekali, contoh (23.5, [0, 2, 1, 3]).
- Hasil wajib sama dengan brute_force_route untuk n kecil (TC-17).
"""
from __future__ import annotations

import math

MAX_POINTS = 16  # restoran + 15 customer


def held_karp(dist: list[list[float]]) -> tuple[float, list[int]]:
    """Tabulation dp[mask][j]; rekonstruksi rute dengan tabel parent.

    State      : dp[mask][j] = waktu minimum mengunjungi titik dalam mask, berakhir di j
    Base case  : dp[1][0] = 0  (mask = 1 berarti hanya titik 0 / restoran)
    Recurrence : dp[mask | 1<<k][k] = min(dp[mask][j] + dist[j][k]), k tidak dalam mask
    Jawaban    : min(dp[FULL][j]) untuk semua j
    Kompleksitas: O(n^2 * 2^n) waktu, O(n * 2^n) memori
    """
    if len(dist) > MAX_POINTS:
        raise ValueError(f"Held-Karp dibatasi {MAX_POINTS} titik (termasuk restoran).")
    n = len(dist)
    if n == 0 or any(len(row) != n for row in dist):
        raise ValueError("Matriks jarak harus persegi dan tidak kosong")
    if any(not math.isfinite(v) or v < 0 for row in dist for v in row):
        raise ValueError("Waktu tempuh harus finite dan tidak negatif")
    if n == 1:
        return 0.0, [0]
    full = (1 << n) - 1
    dp = [[float('inf')] * n for _ in range(full + 1)]
    parent = [[-1] * n for _ in range(full + 1)]
    dp[1][0] = 0.0
    for mask in range(1, full + 1, 2):
        for j in range(n):
            cost = dp[mask][j]
            if not math.isfinite(cost):
                continue
            for k in range(1, n):
                if mask & (1 << k):
                    continue
                next_mask = mask | (1 << k)
                candidate = cost + dist[j][k]
                if candidate < dp[next_mask][k]:
                    dp[next_mask][k] = candidate
                    parent[next_mask][k] = j
    last = 1
    for j in range(2, n):
        if dp[full][j] < dp[full][last]:
            last = j
    cost, route, mask = dp[full][last], [], full
    while last != -1:
        route.append(last)
        previous = parent[mask][last]
        mask ^= 1 << last
        last = previous
    route.reverse()
    return cost, route

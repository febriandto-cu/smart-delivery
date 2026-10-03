"""Baseline brute force untuk DP (Proposal Bagian 9.6). Sudah jadi.

Mencoba semua permutasi urutan customer: O(n * n!). Dipakai sebagai
pembanding performa dan sebagai "kunci jawaban" untuk TC-17.
"""
from __future__ import annotations

from itertools import permutations


def brute_force_route(dist: list[list[float]]) -> tuple[float, list[int]]:
    n = len(dist)
    if n <= 1:
        return 0.0, [0]
    best_cost, best_perm = float("inf"), ()
    for perm in permutations(range(1, n)):
        cost = dist[0][perm[0]]
        for a, b in zip(perm, perm[1:]):
            cost += dist[a][b]
            if cost >= best_cost:
                break
        else:
            best_cost, best_perm = cost, perm
    return best_cost, [0, *best_perm]

"""S7 — M Febri. Held-Karp top-down, pembanding bottom-up dp_route.py.

dist dan hasil sama dengan held_karp: start 0, tanpa pulang, maksimal 16 titik.
Gunakan tabel list [mask][last] dan parent untuk memo/rekonstruksi manual.
State O(n*2^n), transisi O(n), total O(n^2*2^n); catat state dan cache hit.
"""
from src.algorithms.dp_route import MAX_POINTS


def held_karp_memo(dist: list[list[float]]) -> tuple[float, list[int]]:
    if len(dist) > MAX_POINTS:
        raise ValueError(f"Held-Karp dibatasi {MAX_POINTS} titik.")
    raise NotImplementedError("TODO(S7 M Febri): Held-Karp memoization")

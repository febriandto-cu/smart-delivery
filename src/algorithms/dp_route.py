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
    raise NotImplementedError("TODO(DP Owner): held_karp")

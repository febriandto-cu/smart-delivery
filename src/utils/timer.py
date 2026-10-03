"""Alat ukur performa (Proposal Bagian 12). Pemilik: QA & Performance Lead. Sudah jadi."""
from __future__ import annotations

import time
import tracemalloc
from statistics import mean
from typing import Any, Callable


def measure(setup: Callable[[], Any], run: Callable[[Any], Any], repeats: int = 5,
            track_memory: bool = False) -> dict:
    """Jalankan setup() (tidak diukur) lalu run(state) (diukur), diulang `repeats` kali."""
    times, peak = [], 0
    for _ in range(repeats):
        state = setup()
        if track_memory:
            tracemalloc.start()
        start = time.perf_counter()
        run(state)
        elapsed = time.perf_counter() - start
        if track_memory:
            peak = max(peak, tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()
        times.append(elapsed)
    return {"mean_ms": mean(times) * 1000, "min_ms": min(times) * 1000, "peak_kb": peak / 1024}

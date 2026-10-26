"""Alat ukur performa (Proposal Bagian 12). Pemilik: QA & Performance Lead. Sudah jadi."""
from __future__ import annotations

import time
import tracemalloc
from statistics import mean, median
from typing import Any, Callable


def measure(setup: Callable[[], Any], run: Callable[[Any], Any], repeats: int = 5,
            track_memory: bool = False, warmup: int = 1) -> dict:
    """State baru per sampel; warm-up tidak diukur; median untuk laporan UAS.

    Memori diukur pada satu run terpisah agar tracemalloc tidak mengubah
    hasil waktu. Alokasi setup dikecualikan, termasuk saat mengukur memori.
    """
    if repeats < 1 or warmup < 0:
        raise ValueError("repeats harus >= 1 dan warmup >= 0")
    for _ in range(warmup):
        run(setup())
    times, peak = [], 0
    for _ in range(repeats):
        state = setup()
        start = time.perf_counter()
        run(state)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    if track_memory:
        if tracemalloc.is_tracing():
            raise RuntimeError("Pengukuran memori tidak boleh menumpuk tracer aktif")
        state = setup()
        tracemalloc.start()
        try:
            run(state)
            peak = tracemalloc.get_traced_memory()[1]
        finally:
            tracemalloc.stop()
    return {"mean_ms": mean(times) * 1000, "median_ms": median(times) * 1000,
            "min_ms": min(times) * 1000, "peak_kb": peak / 1024,
            "samples_ms": [t * 1000 for t in times], "repeats": repeats,
            "warmup": warmup, "memory_tracked": track_memory}

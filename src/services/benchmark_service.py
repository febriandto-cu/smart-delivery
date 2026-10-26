"""BenchmarkService: eksperimen E1-E5 (Proposal Bagian 12).

Pemilik: QA & Performance Lead. Kerangka sudah jalan; tiap baris struktur data
otomatis berisi hasil setelah modulnya diimplementasi.
"""
from __future__ import annotations

import random
import json
import platform
from datetime import datetime, timezone
from typing import Callable

import pandas as pd

from src.algorithms.brute_force import brute_force_route
from src.algorithms.dp_route import held_karp
from src.baselines import NaiveBST, SortedListPQ, linear_prefix_groups, linear_search
from src.data.generator import (generate_distance_matrix, generate_orders,
                                generate_restaurants)
from src.ds.avl import AVLTree
from src.ds.hash_table import HashTable
from src.ds.max_heap import MaxHeap
from src.ds.trie import Trie
from src.utils.timer import measure

EXPERIMENTS = {
    "E1": "Priority Queue: Max-Heap vs sorted list",
    "E2": "Order search: Hash Table vs linear search",
    "E3": "Prefix search: Trie vs linear startswith",
    "E4": "Ranking (input terurut): AVL Tree vs BST tanpa balancing",
    "E5": "Rute kurir: DP Held-Karp vs brute force",
}
# Di atas batas ini baseline dilewati karena terlalu lama (itu sendiri adalah temuan).
BASELINE_LIMIT = {"E1": 100_000, "E2": 50_000, "E3": 50_000, "E4": 5_000, "E5": 9}
N_QUERIES = 500
SEED = 42


def _row(exp: str, n: int, impl: str, fn: Callable[[], None], repeats: int) -> dict:
    try:
        result = measure(lambda: None, lambda _: fn(), repeats, track_memory=True)
        return {"eksperimen": exp, "n": n, "implementasi": impl,
                "waktu_ms": result["median_ms"], "mean_ms": result["mean_ms"],
                "peak_kb": result["peak_kb"], "repeats": result["repeats"],
                "warmup": result["warmup"], "samples_ms": json.dumps(result["samples_ms"]),
                "catatan": "Memori: run terpisah; setup/index awal tidak termasuk"}
    except NotImplementedError as e:
        return {"eksperimen": exp, "n": n, "implementasi": impl, "waktu_ms": None,
                "catatan": f"belum diimplementasi ({e})"}


def _skipped(exp: str, n: int, impl: str) -> dict:
    return {"eksperimen": exp, "n": n, "implementasi": impl, "waktu_ms": None,
            "catatan": f"dilewati: di atas batas baseline {BASELINE_LIMIT[exp]}"}


def run_experiment(exp: str, sizes: list[int], repeats: int = 5) -> pd.DataFrame:
    if exp not in EXPERIMENTS:
        raise ValueError(f"Eksperimen tidak dikenal: {exp}")
    if repeats < 5:
        raise ValueError("Guideline UAS mensyaratkan minimal 5 pengulangan")
    if not sizes or any(n < 1 for n in sizes):
        raise ValueError("Ukuran eksperimen harus positif dan tidak kosong")
    rows = []
    rng = random.Random(SEED)
    for n in sizes:
        limit_ok = n <= BASELINE_LIMIT[exp]

        if exp == "E1":
            restaurants = generate_restaurants(50, SEED)
            keys = [o.max_heap_key() for o in generate_orders(n, restaurants, SEED)]

            def heap_run():
                h = MaxHeap()
                for k in keys:
                    h.insert(k)
                for _ in keys:
                    h.extract_max()

            def base_run():
                pq = SortedListPQ()
                for k in keys:
                    pq.insert(k)
                for _ in keys:
                    pq.extract_max()

            rows.append(_row(exp, n, "Max-Heap", heap_run, repeats))
            rows.append(_row(exp, n, "Sorted list", base_run, repeats) if limit_ok
                        else _skipped(exp, n, "Sorted list"))

        elif exp == "E2":
            restaurants = generate_restaurants(50, SEED)
            orders = generate_orders(n, restaurants, SEED)
            queries = [rng.choice(orders).order_id for _ in range(N_QUERIES - 50)]
            queries += [f"ORD-X{i}" for i in range(50)]  # kunci yang tidak ada
            try:
                table = HashTable()
                for o in orders:
                    table.put(o.order_id, o)
                rows.append(_row(exp, n, "Hash Table",
                                 lambda: [table.get(q) for q in queries], repeats))
            except NotImplementedError as e:
                rows.append({"eksperimen": exp, "n": n, "implementasi": "Hash Table",
                             "waktu_ms": None, "catatan": f"belum diimplementasi ({e})"})
            rows.append(_row(exp, n, "Linear search",
                             lambda: [linear_search(orders, q) for q in queries], repeats)
                        if limit_ok else _skipped(exp, n, "Linear search"))

        elif exp == "E3":
            names = [r.name for r in generate_restaurants(n, SEED)]
            prefixes = [rng.choice(names)[: rng.randint(1, 6)] for _ in range(N_QUERIES)]
            try:
                trie = Trie()
                for i, name in enumerate(names):
                    trie.insert(name, str(i))
                rows.append(_row(exp, n, "Trie",
                                 lambda: [trie.starts_with(p) for p in prefixes], repeats))
            except NotImplementedError as e:
                rows.append({"eksperimen": exp, "n": n, "implementasi": "Trie",
                             "waktu_ms": None, "catatan": f"belum diimplementasi ({e})"})
            rows.append(_row(exp, n, "Linear startswith",
                             lambda: [linear_prefix_groups(names, p) for p in prefixes], repeats)
                        if limit_ok else _skipped(exp, n, "Linear startswith"))

        elif exp == "E4":
            keys = sorted(r.ranking_key() for r in generate_restaurants(n, SEED))

            def avl_run():
                t = AVLTree()
                for k in keys:
                    t.insert(k, None)
                t.top_k(10)

            def bst_run():
                t = NaiveBST()
                for k in keys:
                    t.insert(k, None)
                t.top_k(10)

            rows.append(_row(exp, n, "AVL Tree", avl_run, repeats))
            rows.append(_row(exp, n, "BST tanpa balancing", bst_run, repeats) if limit_ok
                        else _skipped(exp, n, "BST tanpa balancing"))

        elif exp == "E5":
            dist = generate_distance_matrix(n, SEED)
            rows.append(_row(exp, n, "DP Held-Karp", lambda: held_karp(dist), repeats))
            rows.append(_row(exp, n, "Brute force", lambda: brute_force_route(dist), repeats)
                        if limit_ok else _skipped(exp, n, "Brute force"))

        else:
            raise ValueError(f"Eksperimen tidak dikenal: {exp}")
    frame = pd.DataFrame(rows)
    frame["seed"] = SEED
    frame["python"] = platform.python_version()
    frame["platform"] = platform.platform()
    frame["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    frame["statistik"] = "median"
    return frame

"""Bukti kecil yang dihitung ulang dan ekspor snapshot; tidak mengubah data aktif."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import io
import json
import platform
import zipfile

import pandas as pd

from src.algorithms.brute_force import brute_force_route
from src.algorithms.dp_route import held_karp
from src.ds.avl import AVLTree
from src.ds.hash_table import HashTable
from src.ds.trie import Trie
from src.services.order_demo import clock_label, create_demo


def dataset_frames(data: dict) -> dict[str, pd.DataFrame]:
    orders = [{"order_id": o.order_id, "customer_name": o.customer_name,
        "restaurant_id": o.restaurant_id, "items_json": json.dumps(o.items, ensure_ascii=False),
        "priority": o.priority_level.name, "priority_level": int(o.priority_level),
        "max_heap_score": 4 - int(o.priority_level), "created_at_minutes": o.created_at,
        "created_at_hhmm": clock_label(o.created_at),
        "delivery_x_km": o.delivery_location[0], "delivery_y_km": o.delivery_location[1],
        "status": o.status.value} for o in data.get("orders", [])]
    restaurants = [{"restaurant_id": r.restaurant_id, "name": r.name, "rating": r.rating,
        "total_orders": r.total_orders, "x_km": r.location[0], "y_km": r.location[1]}
        for r in data.get("restaurants", [])]
    menus = [{"menu_id": m.menu_id, "restaurant_id": m.restaurant_id, "name": m.name,
              "price_rupiah": m.price} for m in data.get("menus", [])]
    return {
        "orders": pd.DataFrame(orders, columns=["order_id", "customer_name", "restaurant_id",
            "items_json", "priority", "priority_level", "max_heap_score", "created_at_minutes",
            "created_at_hhmm", "delivery_x_km", "delivery_y_km", "status"]),
        "restaurants": pd.DataFrame(restaurants, columns=["restaurant_id", "name", "rating", "total_orders", "x_km", "y_km"]),
        "menus": pd.DataFrame(menus, columns=["menu_id", "restaurant_id", "name", "price_rupiah"]),
    }


def collect_cases() -> list[dict]:
    """Jalankan delapan kasus deterministik menggunakan struktur asli proyek.

    expected adalah oracle/kontrak eksplisit. Exception dicatat sebagai gagal,
    sehingga satu modul rusak tidak menyembunyikan hasil modul yang lain.
    """
    cases = []
    def run(case_id, owner, claim, inputs, expected, operation):
        try:
            actual, details = operation()
            error = ""
        except Exception as exc:
            actual, details, error = None, {}, f"{type(exc).__name__}: {exc}"
        cases.append({"id": case_id, "owner": owner, "claim": claim, "input": inputs,
            "expected": expected, "actual": actual, "passed": not error and actual == expected,
            "error": error, "details": details})

    def heap_case():
        service, orders = create_demo()
        initial = list(service.queue.heap._data)
        valid = service.queue.heap.is_heap()
        route = []
        while len(service.queue):
            order = service.dispatch()
            if order:
                route.append(order.order_id)
            valid = valid and service.queue.heap.is_heap()
        return {"order_ids": route, "heap_valid": valid}, {"initial_heap": initial,
            "input_orders": dataset_frames({"orders": orders})["orders"].drop(columns="status").to_dict("records")}
    run("PQ-FIFO", "Febri Anggoro", "Urgent didahulukan; timestamp sama mengikuti FIFO.",
        [{"id": "DEMO-01", "priority": "NORMAL", "minute": 540},
         {"id": "DEMO-02", "priority": "HIGH", "minute": 541},
         {"id": "DEMO-03", "priority": "URGENT", "minute": 542},
         {"id": "DEMO-04", "priority": "URGENT", "minute": 542}],
        {"order_ids": ["DEMO-03", "DEMO-04", "DEMO-02", "DEMO-01"], "heap_valid": True}, heap_case)

    def hash_case():
        table = HashTable(capacity=3, max_load=100)
        for i in range(8):
            table.put(f"ORD-{i}", i)
        before = [{"bucket": i, "keys": [k for k, _ in b]} for i, b in enumerate(table.buckets)]
        found = table.get("ORD-5")
        removed = table.remove("ORD-5")
        actual = {"found": found, "removed": removed, "after_delete": table.get("ORD-5"),
            "other_keys_intact": all(table.get(f"ORD-{i}") == i for i in range(8) if i != 5),
            "collision_present": any(len(b["keys"]) > 1 for b in before)}
        return actual, {"buckets_before_delete": before, "stats_after_delete": table.stats()}
    run("HASH-COLLISION", "Rigan", "Chaining menangani collision dan delete menjaga key lain.",
        {"capacity": 3, "max_load": 100, "pairs": [[f"ORD-{i}", i] for i in range(8)], "remove": "ORD-5"},
        {"found": 5, "removed": True, "after_delete": None, "other_keys_intact": True,
         "collision_present": True}, hash_case)

    def trie_case():
        trie = Trie()
        for word, oid in [("Ayam Geprek", "R1"), ("Ayam Bakar", "R2"), ("Bakso", "R3")]:
            trie.insert(word, oid)
        return {"words": [w for w, _ in trie.starts_with("AY")],
            "missing_prefix": trie.starts_with("zz"), "partial_is_word": trie.search("ayam")}, {
            "prefix_path": ["root", "a", "y"], "word_count": trie.word_count, "node_count": trie.node_count}
    run("TRIE-PREFIX", "Rendi", "Prefix tidak peka huruf besar; prefix berbeda dari kata lengkap.",
        {"words": ["Ayam Geprek", "Ayam Bakar", "Bakso"], "prefix": "AY"},
        {"words": ["ayam bakar", "ayam geprek"], "missing_prefix": [], "partial_is_word": False}, trie_case)

    rotations = {"LL": [4.8, 4.5, 4.2], "RR": [4.2, 4.5, 4.8],
                 "LR": [4.8, 4.2, 4.5], "RL": [4.2, 4.8, 4.5]}
    for kind, ratings in rotations.items():
        def avl_case(kind=kind, ratings=ratings):
            tree, trace = AVLTree(), []
            for i, rating in enumerate(ratings):
                tree.insert((rating, f"R{i}"), rating)
                trace.append({"insert": rating, "root": tree.root.key[0], "valid": tree.check_avl()})
            actual = {"root_rating": tree.root.key[0], "inorder": [k[0] for k in tree.inorder()],
                "valid_after_each_insert": all(r["valid"] for r in trace),
                "rotation_logged": any(log.startswith(kind) for log in tree.rotation_log)}
            return actual, {"trace": trace, "rotation_log": tree.rotation_log}
        run(f"AVL-{kind}", "Febri Andri", f"Rotasi {kind} menjaga BST, stored height, balance dan ukuran.",
            {"ratings": ratings}, {"root_rating": 4.5, "inorder": [4.2, 4.5, 4.8],
            "valid_after_each_insert": True, "rotation_logged": True}, avl_case)

    dist = [[0, 4, 6, 9], [4, 0, 3, 7], [6, 3, 0, 2], [9, 7, 2, 0]]
    def dp_case():
        cost, route = held_karp(dist)
        oracle, _ = brute_force_route(dist)
        return {"cost": cost, "oracle_cost": oracle, "valid_route": route[0] == 0 and sorted(route) == [0, 1, 2, 3],
            "reconstructed_cost": sum(dist[a][b] for a, b in zip(route, route[1:]))}, {"route": route, "matrix": dist}
    run("DP-ORACLE", "M Febri", "Held-Karp merekonstruksi rute dengan biaya sama dengan brute force.",
        {"matrix_minutes": dist, "return_to_restaurant": False},
        {"cost": 9, "oracle_cost": 9, "valid_route": True, "reconstructed_cost": 9}, dp_case)
    return cases


def evidence_summary(cases: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([{"Kasus": c["id"], "Pemateri": c["owner"], "Klaim yang diperiksa": c["claim"],
        "Hasil": "Lulus" if c["passed"] else "Gagal", "Error": c["error"]} for c in cases])


def evidence_bundle(frames: dict[str, pd.DataFrame], metadata: dict, cases: list[dict],
                    events: list[dict], benchmarks: dict[str, pd.DataFrame], test_log: str = "") -> bytes:
    """Arsip snapshot berisi data mentah, hasil nyata dan checksum; tidak menulis ke disk."""
    files = {f"dataset/{name}.csv": frame.to_csv(index=False).encode("utf-8-sig") for name, frame in frames.items()}
    files["evidence/checks.csv"] = evidence_summary(cases).to_csv(index=False).encode("utf-8-sig")
    files["evidence/cases.json"] = json.dumps(cases, ensure_ascii=False, indent=2).encode("utf-8")
    if events:
        files["evidence/actions.csv"] = pd.DataFrame(events).to_csv(index=False).encode("utf-8-sig")
    for name, frame in benchmarks.items():
        files[f"benchmarks/{name}.csv"] = frame.to_csv(index=False).encode("utf-8-sig")
    if test_log:
        files["evidence/pytest-log.txt"] = test_log.encode("utf-8")
    manifest = {**metadata, "exported_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "counts": {name: len(frame) for name, frame in frames.items()},
        "case_scope": "Delapan kasus kecil fondasi UTS; bukan seluruh rubrik UAS atau benchmark.",
        "files_sha256": {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}}
    files["metadata.json"] = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    files["README.txt"] = (
        "Snapshot bukti Smart Delivery. Sumber dan waktu ekspor ada di metadata.json.\n"
        "Dataset aplikasi dapat berubah karena tambah/proses/batal order dan update rating.\n"
        "Kasus algoritma memakai input kecil terpisah, dapat dilihat lengkap pada cases.json.\n"
        "Benchmark/log hanya disertakan jika tersedia di session saat ekspor.\n"
        "Berkas ini tidak menggantikan screenshot eksekusi nyata dan laporan UAS.\n").encode("utf-8")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return output.getvalue()

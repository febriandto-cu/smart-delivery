"""Cek cepat status implementasi tiap modul, ditampilkan di halaman Beranda."""
from __future__ import annotations

from src.algorithms.dp_route import held_karp
from src.ds.avl import AVLTree
from src.ds.hash_table import HashTable
from src.ds.heap import MinHeap
from src.ds.trie import Trie


def _heap() -> None:
    h = MinHeap()
    for k in [(3, 1.0, "c"), (1, 5.0, "b"), (1, 2.0, "a")]:
        h.insert(k)
    assert [h.extract_min()[2] for _ in range(3)] == ["a", "b", "c"]


def _hash() -> None:
    t = HashTable()
    t.put("ORD-1", 1)
    assert t.get("ORD-1") == 1 and t.get("ORD-2") is None


def _trie() -> None:
    t = Trie()
    t.insert("Bakso Pak Kumis", "R1")
    assert [w for w, _ in t.starts_with("bak")] == ["bakso pak kumis"]


def _avl() -> None:
    t = AVLTree()
    for k in [(4.2, "a"), (4.5, "b"), (4.8, "c")]:
        t.insert(k, k[1])
    assert t.root.key == (4.5, "b") and t.top_k(1)[0][0] == (4.8, "c")


def _dp() -> None:
    dist = [[0, 1, 4], [1, 0, 2], [4, 2, 0]]
    cost, route = held_karp(dist)
    assert cost == 3 and route == [0, 1, 2]


MODULES = [
    ("Heap & Priority Queue", "Heap & PQ Engineer", "src/ds/heap.py", _heap),
    ("Hash Table", "Hash Table Engineer", "src/ds/hash_table.py", _hash),
    ("Trie", "Trie Engineer", "src/ds/trie.py", _trie),
    ("AVL Tree", "AVL Tree Engineer", "src/ds/avl.py", _avl),
    ("Dynamic Programming", "DP Engineer", "src/algorithms/dp_route.py", _dp),
]


def module_status() -> list[dict]:
    out = []
    for name, owner, path, probe in MODULES:
        try:
            probe()
            status = "Siap"
        except NotImplementedError:
            status = "Belum diimplementasi"
        except Exception as e:  # noqa: BLE001 - tampilkan error apa pun ke tim
            status = f"Error: {type(e).__name__}"
        out.append({"Modul": name, "Pemilik": owner, "File": path, "Status": status})
    return out

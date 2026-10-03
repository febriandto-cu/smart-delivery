"""TC-12 s.d. TC-15 (Proposal Bagian 11). Pemilik: AVL Tree Engineer."""
import random

from src.ds.avl import AVLTree


def build(ratings) -> AVLTree:
    t = AVLTree()
    for i, r in enumerate(ratings):
        t.insert((r, f"R{i}"), f"resto-{i}")
    return t


def test_tc12_rotasi_ll():
    t = build([4.8, 4.5, 4.2])
    assert t.root.key[0] == 4.5 and t.is_balanced()
    assert any(log.startswith("LL") for log in t.rotation_log)


def test_tc13_rotasi_rr():
    t = build([4.2, 4.5, 4.8])
    assert t.root.key[0] == 4.5 and t.is_balanced()
    assert any(log.startswith("RR") for log in t.rotation_log)


def test_tc14_rotasi_lr():
    t = build([4.8, 4.2, 4.5])
    assert t.root.key[0] == 4.5 and t.is_balanced()
    assert any(log.startswith("LR") for log in t.rotation_log)


def test_tc15_rotasi_rl():
    t = build([4.2, 4.8, 4.5])
    assert t.root.key[0] == 4.5 and t.is_balanced()
    assert any(log.startswith("RL") for log in t.rotation_log)


def test_seimbang_dan_terurut_setelah_banyak_insert():
    ratings = [round(random.uniform(3, 5), 1) for _ in range(1000)]
    t = build(ratings)
    assert t.is_balanced() and len(t) == 1000
    assert t.inorder() == sorted(t.inorder())


def test_input_terurut_tetap_seimbang():
    t = build([3.0 + i * 0.001 for i in range(1000)])
    assert t.height(t.root) <= 15  # 1,44 * log2(1000) ~ 14,4


def test_top_k_dan_range_query():
    t = build([4.1, 4.9, 3.5, 4.7, 5.0])
    assert [k[0] for k, _ in t.top_k(3)] == [5.0, 4.9, 4.7]
    assert [k[0] for k, _ in t.range_query(4.7)] == [5.0, 4.9, 4.7]


def test_delete_dan_search():
    t = build([4.1, 4.9, 3.5, 4.7, 5.0, 4.4, 3.9])
    assert t.delete((4.9, "R1")) is True
    assert t.search((4.9, "R1")) is None
    assert t.delete((4.9, "R1")) is False
    assert t.is_balanced() and len(t) == 6
    assert t.search((5.0, "R4")) == "resto-4"

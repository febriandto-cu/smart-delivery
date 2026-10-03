"""TC-01 s.d. TC-04 (Proposal Bagian 11). Pemilik: Heap & PQ Engineer."""
import random

import pytest

from src.ds.heap import MinHeap


def test_tc01_keluar_sesuai_prioritas():
    h = MinHeap()
    h.insert((3, 1.0, "normal"))
    h.insert((1, 2.0, "urgent"))
    h.insert((2, 3.0, "high"))
    assert [h.extract_min()[2] for _ in range(3)] == ["urgent", "high", "normal"]


def test_tc02_fifo_pada_level_sama():
    h = MinHeap()
    h.insert((2, 605.0, "high_1005"))
    h.insert((2, 600.0, "high_1000"))
    assert h.extract_min()[2] == "high_1000"


def test_tc03_extract_heap_kosong():
    h = MinHeap()
    assert h.extract_min() is None
    assert h.peek() is None


@pytest.mark.opsional
def test_tc04_update_priority():
    h = MinHeap()
    for i in range(10):
        h.insert((3, float(i), f"n{i}"))
    h.insert((2, 0.0, "h0"))
    assert h.update_priority("n7", 1) is True
    assert h.peek()[2] == "n7"


def test_acak_selalu_terurut():
    keys = [(random.randint(1, 3), random.random(), str(i)) for i in range(500)]
    h = MinHeap()
    for k in keys:
        h.insert(k)
    assert [h.extract_min() for _ in keys] == sorted(keys)


def test_build_heap():
    keys = [(random.randint(1, 3), random.random(), str(i)) for i in range(200)]
    h = MinHeap()
    h.build_heap(keys)
    assert [h.extract_min() for _ in keys] == sorted(keys)

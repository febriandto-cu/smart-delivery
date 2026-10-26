"""MaxHeap pilihan tim: invarian, oracle, perubahan skor, dan FIFO dispatcher."""
import random

import pytest

from src.ds.heap import OrderPriorityQueue
from src.ds.max_heap import MaxHeap, heap_sort
from src.models import Order, Priority


def order(oid, priority, minute):
    return Order(oid, "Test", "R1", [], priority, minute, (0, 0))


def test_max_heap_matches_descending_oracle_after_every_operation():
    rng = random.Random(42)
    keys = [(rng.randrange(1, 4), -rng.random(), str(i)) for i in range(200)]
    heap = MaxHeap(trace=True)
    for key in keys:
        heap.insert(key)
        assert heap.is_heap()
    actual = []
    while len(heap):
        actual.append(heap.extract_max())
        assert heap.is_heap()
    assert actual == sorted(keys, reverse=True)
    assert heap.extract_max() is None and heap.peek() is None
    assert heap.comparisons > 0 and heap.trace


def test_build_heap_and_sort_leave_input_unchanged():
    keys = [(1, -10, "a"), (3, -20, "b"), (2, -5, "c"), (3, -1, "d")]
    original = keys.copy()
    heap = MaxHeap()
    heap.build_heap(iter(keys))
    assert heap.is_heap() and heap.peek() == max(keys)
    assert heap_sort(keys) == sorted(keys)
    assert keys == original
    heap.build_heap([])
    assert heap.is_empty() and heap_sort([]) == []


def test_priority_change_promotes_and_demotes_without_changing_tie_breakers():
    heap = MaxHeap()
    for o in [order("normal", Priority.NORMAL, 1), order("high", Priority.HIGH, 2)]:
        heap.insert(o.max_heap_key())
    assert heap.update_priority("normal", Priority.URGENT)
    assert heap.peek() == (3, -1, "normal")
    assert heap.update_priority("normal", Priority.NORMAL)
    assert heap.peek()[-1] == "high" and heap.is_heap()
    assert not heap.update_priority("missing", Priority.URGENT)
    with pytest.raises(ValueError):
        heap.update_priority("high", 4)


def test_queue_urgent_first_older_timestamp_first_and_sequence_before_id():
    queue = OrderPriorityQueue()
    assert isinstance(queue.heap, MaxHeap)
    assert queue.pop() is None and queue.peek() is None
    for o in [order("normal", Priority.NORMAL, 0), order("high", Priority.HIGH, 0),
              order("z-first", Priority.URGENT, 10), order("a-second", Priority.URGENT, 10),
              order("older", Priority.URGENT, 5)]:
        queue.push(o)
    assert queue.peek() == "older"
    assert [queue.pop() for _ in range(5)] == ["older", "z-first", "a-second", "high", "normal"]
    assert len(queue) == 0


def test_sorted_list_baseline_produces_same_max_order():
    from src.baselines import SortedListPQ
    keys = [o.max_heap_key() for o in [order("a", Priority.NORMAL, 0),
            order("b", Priority.URGENT, 7), order("c", Priority.URGENT, 2)]]
    heap, baseline = MaxHeap(), SortedListPQ()
    for key in keys:
        heap.insert(key)
        baseline.insert(key)
    assert [heap.extract_max() for _ in keys] == [baseline.extract_max() for _ in keys]

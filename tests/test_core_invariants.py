"""Cross-check operasi campuran, invarian penuh dan input DP terarah."""
import random

import pytest

from src.algorithms.brute_force import brute_force_route
from src.algorithms.dp_route import held_karp
from src.ds.avl import AVLTree
from src.ds.hash_table import HashTable
from src.ds.trie import Trie


def test_avl_mixed_updates_deletes_validate_stored_heights_and_order():
    rng, tree, reference = random.Random(42), AVLTree(), {}
    for _ in range(500):
        key = (rng.randrange(30) / 10, str(rng.randrange(40)))
        if rng.random() < 0.65:
            value = rng.randrange(1000)
            tree.insert(key, value)
            reference[key] = value
        else:
            assert tree.delete(key) == (key in reference)
            reference.pop(key, None)
        assert tree.check_avl()
        assert len(tree) == len(reference)
        assert tree.inorder() == sorted(reference)
        assert tree.top_k(5) == sorted(reference.items(), reverse=True)[:5]
    for key in list(reference):
        assert tree.delete(key)
        assert tree.check_avl()
    assert tree.root is None and len(tree) == 0


def test_hash_polynomial_contract_and_low_load_rehash_preserve_all_values():
    table = HashTable(capacity=2, max_load=0.1)
    for i in range(40):
        key = f"key-{i}"
        expected = sum(ord(c) * 31**j for j, c in enumerate(key)) % table.capacity
        assert table.hash_function(key) == expected
        table.put(key, i)
        assert table.load_factor() <= 0.1
    assert all(table.get(f"key-{i}") == i for i in range(40))


def test_trie_long_words_limit_zero_and_result_ids_are_copied():
    trie = Trie()
    trie.insert("  BAKSO   A ", "R1")
    trie.insert("bakso a", "R1")
    trie.insert("bakso a", "R2")
    result = trie.starts_with(" BAKSO ")
    assert result == [("bakso a", ["R1", "R2"])]
    result[0][1].clear()
    assert trie.starts_with("bakso")[0][1] == ["R1", "R2"]
    assert trie.starts_with("", limit=0) == []
    trie.insert("x" * 1500, "long")
    assert trie.starts_with("x")[0][0] == "x" * 1500


def test_dp_matches_oracle_on_asymmetric_and_zero_cost_matrices():
    rng = random.Random(24)
    for n in range(2, 7):
        dist = [[0 if i == j else rng.randrange(20) for j in range(n)] for i in range(n)]
        cost, route = held_karp(dist)
        oracle, _ = brute_force_route(dist)
        assert cost == pytest.approx(oracle)
        assert route[0] == 0 and sorted(route) == list(range(n))
        assert sum(dist[a][b] for a, b in zip(route, route[1:])) == pytest.approx(cost)
    assert held_karp([[0, 0], [0, 0]]) == (0, [0, 1])
    for invalid in [[], [[0, 1]], [[0, -1], [1, 0]], [[0, float("nan")], [1, 0]]]:
        with pytest.raises(ValueError):
            held_karp(invalid)

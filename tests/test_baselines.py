"""Sanity check baseline & generator (sudah lulus sejak awal)."""
from src.algorithms.brute_force import brute_force_route
from src.baselines import NaiveBST, SortedListPQ, linear_prefix_search
from src.data.generator import generate_distance_matrix, generate_orders, generate_restaurants


def test_generator_deterministik():
    a = generate_restaurants(50, seed=1)
    b = generate_restaurants(50, seed=1)
    assert [r.name for r in a] == [r.name for r in b]
    assert len({o.order_id for o in generate_orders(500, a)}) == 500


def test_matriks_simetris():
    d = generate_distance_matrix(5)
    assert all(d[i][j] == d[j][i] for i in range(6) for j in range(6))


def test_brute_force_kecil():
    dist = [[0, 1, 4], [1, 0, 2], [4, 2, 0]]
    assert brute_force_route(dist) == (3, [0, 1, 2])


def test_baselines():
    pq = SortedListPQ()
    for k in [(3, 1.0, "a"), (1, 1.0, "b")]:
        pq.insert(k)
    assert pq.extract_min()[2] == "b"
    bst = NaiveBST()
    for i in range(100):
        bst.insert(i, i)
    assert bst.height() == 100 and bst.top_k(2) == [(99, 99), (98, 98)]
    assert linear_prefix_search(["Bakso A", "Sate B"], "ba") == ["Bakso A"]

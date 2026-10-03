"""TC-16 dan TC-17 (Proposal Bagian 11). Pemilik: DP Engineer."""
import pytest

from src.algorithms.brute_force import brute_force_route
from src.algorithms.dp_route import held_karp
from src.data.generator import generate_distance_matrix


def test_tc16_satu_customer():
    assert held_karp([[0, 7.5], [7.5, 0]]) == (7.5, [0, 1])


def test_tanpa_customer():
    cost, route = held_karp([[0]])
    assert cost == 0 and route == [0]


@pytest.mark.parametrize("n", range(2, 9))
def test_tc17_sama_dengan_brute_force(n):
    dist = generate_distance_matrix(n, seed=n)
    dp_cost, dp_route = held_karp(dist)
    bf_cost, _ = brute_force_route(dist)
    assert dp_cost == pytest.approx(bf_cost)
    assert sorted(dp_route) == list(range(n + 1)) and dp_route[0] == 0
    route_cost = sum(dist[a][b] for a, b in zip(dp_route, dp_route[1:]))
    assert route_cost == pytest.approx(dp_cost)


def test_batas_jumlah_titik():
    with pytest.raises(ValueError):
        held_karp(generate_distance_matrix(20))

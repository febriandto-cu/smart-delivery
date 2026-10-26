"""S13 — pemilik belum ditentukan. Kapasitas integer >=0, directed graph.

capacity matriks n x n; source != sink. Residual reverse edge WAJIB ada.
Return {value, flow, residual, augmenting_paths, source_side, cut_capacity}.
flow berupa matriks aliran net antisymmetric, -cap[v][u] <= f[u][v] <= cap[u][v].
Validator mengecek bound, konservasi semua nonterminal, value source/sink,
serta kesamaan max-flow/min-cut. Jangan menganggap biaya = kapasitas.
"""


def ford_fulkerson(capacity: list[list[int]], source: int, sink: int) -> dict:
    """DFS augmenting path manual, O(E*f) pada kapasitas integer."""
    raise NotImplementedError("TODO(S13 pemilik belum ditentukan): Ford-Fulkerson DFS")


def edmonds_karp(capacity: list[list[int]], source: int, sink: int) -> dict:
    """BFS augmenting path manual, O(V*E^2)."""
    raise NotImplementedError("TODO(S13 pemilik belum ditentukan): Edmonds-Karp BFS")

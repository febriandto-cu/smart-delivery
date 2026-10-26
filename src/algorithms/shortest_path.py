"""S12 — pemilik belum ditentukan. Directed graph; biaya promo dapat negatif, waktu tidak.

Vertex 0..n-1, edges (u,v,cost). Unreachable = float('inf'). Bellman-Ford
hanya mendeteksi siklus negatif reachable dari source. Floyd menandai pair
yang terpengaruh siklus negatif; jangan tampilkan rute optimum pair tersebut.
"""


def bellman_ford(n: int, edges: list[tuple[int, int, float]], source: int) -> dict:
    """O(VE). Return distances, predecessors, negative_cycle, trace.

    negative_cycle adalah list vertex satu siklus reachable, atau [];
    definisikan juga affected_vertices agar rekonstruksi dapat ditolak.
    """
    raise NotImplementedError("TODO(S12 pemilik belum ditentukan): Bellman-Ford")


def floyd_warshall(n: int, edges: list[tuple[int, int, float]]) -> dict:
    """O(V^3), O(V^2). Return distances, next, negative_vertices, trace.

    Minimum pada parallel edges; diagonal = min(0, self-loop weight).
    Trace matriks per k hanya untuk n kecil agar tidak membengkakkan memori.
    """
    raise NotImplementedError("TODO(S12 pemilik belum ditentukan): Floyd-Warshall")

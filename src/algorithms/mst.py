"""S11 — pemilik belum ditentukan. Graf undirected, vertex 0..n-1, edge (u,v,cost).

Kruskal: manual merge sort + UnionFind, O(E log E).
Prim: heap manual (adapter key ke MinHeap), O(E log V) pada graf sederhana.
Default tolak disconnected; forest=True mengembalikan minimum spanning forest.
Return {edges: list[tuple], weight: float, components: int, trace: list[dict]}.
"""


def kruskal(n: int, edges: list[tuple[int, int, float]], forest: bool = False) -> dict:
    raise NotImplementedError("TODO(S11 pemilik belum ditentukan): Kruskal")


def prim(n: int, edges: list[tuple[int, int, float]], forest: bool = False) -> dict:
    raise NotImplementedError("TODO(S11 pemilik belum ditentukan): Prim dengan heap manual")

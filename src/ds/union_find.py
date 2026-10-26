"""S11 — pemilik belum ditentukan. Array parent/rank; path compression dan union by rank."""


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, vertex: int) -> int:
        raise NotImplementedError("TODO(S11 pemilik belum ditentukan): find/path compression")

    def union(self, first: int, second: int) -> bool:
        """False jika sudah terhubung; True jika dua komponen digabung."""
        raise NotImplementedError("TODO(S11 pemilik belum ditentukan): union by rank")

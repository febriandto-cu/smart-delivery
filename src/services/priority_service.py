"""S2 — Febri Anggoro, integrasi Husnu.

Kontrak tambahan; OrderPriorityQueue lama tetap kompatibel.
MaxHeap key = (effective_score, -sequence, order_id); Urgent=3, High=2, Normal=1.
Sequence naik saat enqueue; sequence lebih kecil harus menang.
created_at tetap menyimpan menit bisnis, bukan sequence. Aging dihitung dari
jam simulasi monotonik; jangan menggunakan jam dinding saat benchmark.
Rebuild saat aging boleh O(n), nyatakan biaya tersebut secara terbuka.
"""
from src.models import Order


class AgingPriorityQueue:
    def __init__(self, aging_minutes: float = 30.0):
        if aging_minutes <= 0:
            raise ValueError("aging_minutes harus positif")
        self.aging_minutes = aging_minutes

    def enqueue(self, order: Order, now: float) -> None:
        """Catat waktu masuk dan sequence unik; reject ID yang sudah aktif."""
        raise NotImplementedError("TODO(S2 Febri Anggoro): enqueue")

    def change_priority(self, order_id: str, new_level: int) -> bool:
        """Ubah prioritas dasar; False bila ID tidak aktif; sequence tetap."""
        raise NotImplementedError("TODO(S2 Febri Anggoro): change_priority")

    def apply_aging(self, now: float) -> list[dict]:
        """Promosi per interval hingga Urgent; return trace sebelum/sesudah."""
        raise NotImplementedError("TODO(S2 Febri Anggoro): apply_aging")

    def peek(self, now: float) -> Order | None:
        raise NotImplementedError("TODO(S2 Febri Anggoro): peek")

    def dequeue(self, now: float) -> Order | None:
        """Terapkan aging, ambil minimum, simpan trace dan waktu tunggu."""
        raise NotImplementedError("TODO(S2 Febri Anggoro): dequeue")

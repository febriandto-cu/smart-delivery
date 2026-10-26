"""Entitas data sistem (Proposal Bagian 7.2).

Pemilik: System Architect. Perubahan atribut wajib dikabarkan ke seluruh tim,
karena dipakai oleh semua modul.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class Priority(IntEnum):
    """Level data lama: angka kecil lebih urgent; skor Max-Heap = 4-level."""

    URGENT = 1
    HIGH = 2
    NORMAL = 3


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class Order:
    order_id: str
    customer_name: str
    restaurant_id: str
    items: list[str]
    priority_level: Priority
    created_at: float  # menit sejak awal hari, dipakai sebagai tie-breaker FIFO
    delivery_location: tuple[float, float]  # koordinat (x, y) dalam km
    status: OrderStatus = OrderStatus.PENDING

    def heap_key(self) -> tuple[int, float, str]:
        """Kunci MinHeap lama, dipertahankan untuk kompatibilitas/oracle."""
        return (int(self.priority_level), self.created_at, self.order_id)

    def max_heap_key(self) -> tuple[int, float, str]:
        """Skor Urgent=3, High=2, Normal=1; waktu lebih awal menang."""
        return (4 - int(self.priority_level), -self.created_at, self.order_id)


@dataclass
class Restaurant:
    restaurant_id: str
    name: str
    rating: float
    total_orders: int
    location: tuple[float, float]

    def ranking_key(self) -> tuple[float, str]:
        """Kunci AVL Tree: (rating, restaurant_id) agar unik walau rating sama."""
        return (self.rating, self.restaurant_id)


@dataclass
class MenuItem:
    menu_id: str
    restaurant_id: str
    name: str
    price: int  # rupiah


@dataclass
class Courier:
    courier_id: str
    name: str
    current_location: tuple[float, float]
    assigned_orders: list[str] = field(default_factory=list)

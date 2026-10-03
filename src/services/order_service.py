"""OrderService: Hash Table + Priority Queue (Proposal Bagian 7.3, langkah 1-3).

Pemilik: System Architect (wiring). Sudah jadi; berfungsi setelah
hash_table.py dan heap.py diimplementasi.
"""
from __future__ import annotations

from typing import Optional

from src.ds.hash_table import HashTable
from src.ds.heap import OrderPriorityQueue
from src.models import Order, OrderStatus


class OrderService:
    def __init__(self) -> None:
        self.table = HashTable()
        self.queue = OrderPriorityQueue()

    def load(self, orders: list[Order]) -> None:
        for order in orders:
            self.add_order(order)

    def add_order(self, order: Order) -> None:
        self.table.put(order.order_id, order)
        self.queue.push(order)

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.table.get(order_id)

    def cancel_order(self, order_id: str) -> bool:
        """Lazy deletion: order tetap di heap, tetapi dilewati saat dispatch."""
        order = self.get_order(order_id)
        if order is None or order.status != OrderStatus.PENDING:
            return False
        order.status = OrderStatus.CANCELLED
        return True

    def _skip_inactive(self) -> None:
        while len(self.queue):
            order = self.get_order(self.queue.peek())
            if order is not None and order.status == OrderStatus.PENDING:
                return
            self.queue.pop()

    def next_order(self) -> Optional[Order]:
        self._skip_inactive()
        order_id = self.queue.peek()
        return self.get_order(order_id) if order_id else None

    def dispatch(self) -> Optional[Order]:
        self._skip_inactive()
        order_id = self.queue.pop()
        if order_id is None:
            return None
        order = self.get_order(order_id)
        order.status = OrderStatus.PROCESSING
        return order

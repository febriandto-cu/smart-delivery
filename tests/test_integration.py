"""TC-18 (Proposal Bagian 11): alur penuh order -> prioritas -> rute. Pemilik: QA Lead."""
from src.models import Order, OrderStatus, Priority
from src.services.delivery_service import DeliveryService
from src.services.order_service import OrderService


def make(i, level, minute):
    return Order(f"ORD-{i}", "Andi", "R1", ["Bakso"], level, minute, (1.0, 1.0))


def test_tc18_alur_penuh():
    svc = OrderService()
    svc.load([make(1, Priority.NORMAL, 1), make(2, Priority.URGENT, 5),
              make(3, Priority.HIGH, 2), make(4, Priority.URGENT, 3),
              make(5, Priority.NORMAL, 0)])
    assert svc.cancel_order("ORD-4") is True
    order_ids = [svc.dispatch().order_id for _ in range(4)]
    assert order_ids == ["ORD-2", "ORD-3", "ORD-5", "ORD-1"]
    assert svc.get_order("ORD-2").status == OrderStatus.PROCESSING
    assert svc.dispatch() is None

    delivery = DeliveryService()
    result = delivery.optimize(delivery.make_matrix(4))
    assert result["route"][0] == 0 and len(result["route"]) == 5

"""Skenario presentasi terisolasi, menggunakan OrderService dan heap asli."""
from src.ds.max_heap import MaxHeap
from src.models import Order, OrderStatus, Priority
from src.services.order_service import OrderService


def create_demo() -> tuple[OrderService, list[Order]]:
    orders = [
        Order("DEMO-01", "Andi", "R-DEMO", ["Nasi goreng"], Priority.NORMAL, 540, (1, 1)),
        Order("DEMO-02", "Budi", "R-DEMO", ["Bakso"], Priority.HIGH, 541, (2, 1)),
        Order("DEMO-03", "Citra", "R-DEMO", ["Ayam bakar"], Priority.URGENT, 542, (1, 2)),
        Order("DEMO-04", "Dewi", "R-DEMO", ["Soto"], Priority.URGENT, 542, (2, 2)),
    ]
    service = OrderService()
    service.load(orders)
    return service, orders


def queue_preview(service: OrderService, limit: int = 12) -> list[Order]:
    """Simulasikan extract pada salinan heap, tanpa mengambil antrean asli.

    Bukan urutan array heap. Order batal/yang sudah diproses dilewati.
    Biaya tampilan O(n + jumlah pengambilan * log n), bukan biaya peek.
    """
    snapshot = MaxHeap()
    snapshot.build_heap(service.queue.heap._data)
    result = []
    while len(snapshot) and len(result) < limit:
        key = snapshot.extract_max()
        order = service.get_order(key[-1])
        if order is not None and order.status == OrderStatus.PENDING:
            result.append(order)
    return result


def selection_reason(orders: list[Order]) -> str:
    if not orders:
        return "Semua order sudah diambil atau dibatalkan. Tambahkan order untuk mencoba lagi."
    first = orders[0]
    score = 4 - int(first.priority_level)
    if len(orders) == 1:
        return "Ini satu-satunya order yang masih menunggu."
    second = orders[1]
    if first.priority_level != second.priority_level:
        return f"Prioritas {first.priority_level.name.title()} berskor {score}, lebih tinggi daripada order berikutnya."
    if first.created_at < second.created_at:
        return "Prioritas sama. Order ini dipilih karena waktu masuknya lebih awal."
    return "Prioritas dan waktu masuk sama. Order ini masuk antrean lebih dulu (FIFO)."


def clock_label(minutes: float) -> str:
    total = int(minutes)
    return f"{total // 60:02d}:{total % 60:02d}"

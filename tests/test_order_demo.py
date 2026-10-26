"""Urutan yang ditampilkan harus sama dengan pengambilan heap asli."""
from src.services.order_demo import create_demo, queue_preview, selection_reason


def test_queue_preview_is_read_only_and_matches_dispatch_including_cancellation():
    service, records = create_demo()
    before = service.queue.heap._data.copy()
    preview = queue_preview(service)
    assert [o.customer_name for o in preview] == ["Citra", "Dewi", "Budi", "Andi"]
    assert service.queue.heap._data == before
    assert "FIFO" in selection_reason(preview)
    assert service.cancel_order("DEMO-04")
    ids = [o.order_id for o in queue_preview(service)]
    assert ids == [service.dispatch().order_id for _ in range(3)]
    assert queue_preview(service) == []
    assert "Semua order" in selection_reason([])
    assert all(o.customer_name in {"Andi", "Budi", "Citra", "Dewi"} for o in records)

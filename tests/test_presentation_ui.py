"""Alur individu dan operasi yang dahulu terblokir TODO di antarmuka."""
import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.presentation import GUIDES

ENTRYPOINT = Path(__file__).resolve().parents[1] / "app.py"


def test_member_card_opens_correct_guide_and_heap_demo_can_extract_and_reset():
    app = AppTest.from_file(ENTRYPOINT).run(timeout=30)
    app.button(key="member_Febri Anggoro").click().run(timeout=30)
    assert not app.exception
    assert app.selectbox(key="selected_member").value == "Febri Anggoro"
    queue = app.session_state.presentation_queue
    assert queue.peek() == "Urgent-A"
    next(b for b in app.button if b.label == "Ambil order tertinggi").click().run()
    assert app.session_state.presentation_queue.peek() == "Urgent-B"
    next(b for b in app.button if b.label == "Reset simulasi").click().run()
    assert app.session_state.presentation_queue.peek() == "Urgent-A"
    assert not app.exception


def test_every_confirmed_member_has_a_guide_and_rendered_demo():
    app = AppTest.from_file(ENTRYPOINT).run(timeout=30)
    app.switch_page("pages/7_Bagian_Individu.py").run(timeout=30)
    for guide in GUIDES:
        app.selectbox(key="selected_member").set_value(guide.name).run(timeout=30)
        assert not app.exception
        assert any(guide.name in h.value for h in app.header)
        assert any("\n".join(guide.files) == code.value for code in app.code)


def test_add_order_is_shared_with_search_and_cancellation_changes_same_object():
    app = AppTest.from_file(ENTRYPOINT).run(timeout=30)
    app.switch_page("pages/1_Order_Management.py").run(timeout=30)
    next(t for t in app.text_input if t.label == "Nama customer").set_value("Demo Integrasi")
    next(b for b in app.button if b.label == "Tambah order").click().run()
    assert not app.exception
    added = app.session_state.data["orders"][-1]
    assert added.customer_name == "Demo Integrasi"
    app.switch_page("pages/2_Search.py").run(timeout=30)
    next(t for t in app.text_input if t.label == "order_id").set_value(added.order_id).run()
    details = json.loads(app.json[0].value)
    assert details["customer"] == "Demo Integrasi"
    app.switch_page("pages/1_Order_Management.py").run(timeout=30)
    next(t for t in app.text_input if t.label == "order_id yang dibatalkan").set_value(added.order_id)
    next(b for b in app.button if b.label == "Batalkan").click().run()
    assert not app.exception
    assert app.session_state.services["order"].get_order(added.order_id).status.value == "cancelled"

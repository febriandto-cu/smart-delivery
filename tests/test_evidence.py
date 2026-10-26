"""Bukti harus cocok dengan eksekusi, snapshot data dan checksum unduhan."""
import hashlib
import io
import json
from pathlib import Path
import zipfile
import pytest

from streamlit.testing.v1 import AppTest

from src.data.generator import generate_menus, generate_orders, generate_restaurants
from src.services.evidence_service import collect_cases, dataset_frames, evidence_bundle

pytestmark = pytest.mark.usefixtures("csv_dataset")


def test_cases_compute_real_results_and_report_algorithm_failures(monkeypatch):
    cases = collect_cases()
    assert len(cases) == 8 and all(c["passed"] for c in cases)
    assert {c["id"] for c in cases if c["owner"] == "Febri Andri"} == {"AVL-LL", "AVL-RR", "AVL-LR", "AVL-RL"}
    def broken(*args, **kwargs):
        raise RuntimeError("deliberate test failure")
    monkeypatch.setattr("src.services.evidence_service.Trie.starts_with", broken)
    failed = next(c for c in collect_cases() if c["id"] == "TRIE-PREFIX")
    assert not failed["passed"] and "deliberate test failure" in failed["error"]


def test_evidence_zip_contains_full_snapshot_and_valid_checksums():
    restaurants = generate_restaurants(3, seed=7)
    data = {"restaurants": restaurants, "menus": generate_menus(5, restaurants, seed=7),
            "orders": generate_orders(10, restaurants, seed=7)}
    frames = dataset_frames(data)
    cases = collect_cases()
    package = evidence_bundle(frames, {"source": "test", "seed": 7}, cases, [], {})
    with zipfile.ZipFile(io.BytesIO(package)) as archive:
        manifest = json.loads(archive.read("metadata.json"))
        assert manifest["seed"] == 7
        assert manifest["counts"] == {"orders": 10, "restaurants": 3, "menus": 5}
        assert len(json.loads(archive.read("evidence/cases.json"))) == 8
        for name, expected in manifest["files_sha256"].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected
        assert "evidence/pytest-log.txt" not in archive.namelist()
        assert "evidence/actions.csv" not in archive.namelist()
    assert frames["orders"]["max_heap_score"].tolist() == [4 - int(o.priority_level) for o in data["orders"]]


def test_evidence_page_follows_demo_state_and_exports_without_mutating_orders():
    root = Path(__file__).resolve().parents[1]
    app = AppTest.from_file(root / "app.py").run(timeout=30)
    app.switch_page("pages/1_Order_Management.py").run()
    app.radio(key="order_mode").set_value("Demo presentasi").run()
    app.button(key="dispatch_next").click().run()
    count = len(app.session_state.data["orders"])
    app.switch_page("pages/8_Evidence_Dataset.py").run(timeout=30)
    app.radio(key="evidence_source").set_value("Demo presentasi").run()
    assert not app.exception
    assert any("8 dari 8" in h.value for h in app.subheader)
    assert any("Citra" in str(frame.value) for frame in app.dataframe)
    next(b for b in app.button if b.label == "Siapkan paket bukti ZIP").click().run()
    assert not app.exception
    with zipfile.ZipFile(io.BytesIO(app.session_state.evidence_export["data"])) as archive:
        assert json.loads(archive.read("metadata.json"))["counts"]["orders"] == 4
        assert "evidence/actions.csv" in archive.namelist()
    assert len(app.session_state.data["orders"]) == count
    assert app.session_state.guided_demo_service.get_order("DEMO-03").status.value == "processing"
    next(s for s in app.selectbox if s.label == "Bukti untuk anggota").set_value("Atika").run()
    assert not app.exception

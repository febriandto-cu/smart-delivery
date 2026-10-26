"""Uji pendukung UAS; tidak menggantikan tes algoritma milik setiap anggota."""
import json
import tracemalloc

import pytest

from src.models import Order, Priority, Restaurant
from src.baselines import linear_prefix_groups
from src.services.benchmark_service import run_experiment
from src.services.delivery_service import DeliveryService
from src.services.uas_service import session_checklist
from src.uas import SESSIONS, TEAM, PRESENTATION
from src.utils.timer import measure


def test_coverage_and_presentation_follow_confirmed_uts_table():
    assert {s.number for s in SESSIONS} == set(range(1, 14)) - {8}
    assert sum(s.weight for s in SESSIONS) == 70
    assert len(TEAM) == 9 and len(PRESENTATION) == 10
    assert sum(row[3] for row in PRESENTATION) == 28
    assert [row[0] for row in PRESENTATION] == [
        "Atika", "Husnu", "Eka", "Febri Anggoro", "Rigan", "Rendi",
        "Febri Andri", "M Febri", "Daffa", "Atika",
    ]
    assert PRESENTATION[1][2] == "Objectives, functional requirements, arsitektur"
    assert PRESENTATION[2][2] == "Pemetaan fitur ke struktur data"
    assert PRESENTATION[8][2] == "Complexity, testing, eksperimen"
    assert all(s.owner == "Belum ditentukan" for s in SESSIONS
               if s.number in {6, 9, 10, 11, 12, 13})
    assert next(s for s in SESSIONS if s.number == 13).min_tests == 5


def test_prefix_benchmark_groups_duplicate_names_before_limiting():
    names = ["Bakso B", "  BAKSO   A ", "Bakso A", "Sate"]
    assert linear_prefix_groups(names, "  BAKSO ", 1) == [("bakso a", ["1", "2"])]
    assert linear_prefix_groups(names, "", 0) == []


def test_audit_does_not_treat_stubs_or_empty_evidence_as_ready(tmp_path):
    spec = SESSIONS[0]
    for filename in spec.files:
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('def run():\n    raise NotImplementedError("pending")\n', encoding="utf-8")
    folder = tmp_path / "docs/evidence/S01/visual"
    folder.mkdir(parents=True)
    (folder / "empty.png").write_bytes(b"")
    (folder / ".gitkeep").write_text("keep")
    (folder / "diagram.svg").write_text("<svg/>")
    rows = session_checklist(tmp_path)
    assert rows[0]["Kode"] == "Kerangka / TODO"
    assert rows[0]["TODO"] == 2
    assert rows[0]["visual"] == 1
    assert rows[1]["Kode"] == "File belum tersedia"
    assert rows[0]["File tes tersedia"] == 0
    (tmp_path / spec.files[0]).write_text("def invalid(:", encoding="utf-8")
    broken = session_checklist(tmp_path)[0]
    assert broken["Kode"] == "Error sintaks/encoding" and spec.files[0] in broken["Error"]


def test_measure_excludes_warmup_and_returns_median_with_fresh_state(monkeypatch):
    clock = iter([0, 3, 10, 11, 20, 22])
    monkeypatch.setattr("src.utils.timer.time.perf_counter", lambda: next(clock))
    seen = []
    def run(state):
        assert not state
        state.append(1)
        seen.append(state)
    result = measure(list, run, repeats=3, warmup=1)
    assert result["samples_ms"] == [3000, 1000, 2000]
    assert result["median_ms"] == 2000
    assert len(seen) == 4
    assert len({id(s) for s in seen}) == 4


def test_memory_run_does_not_trace_timing_samples_and_cleans_up_on_failure():
    seen = []
    def run(_):
        seen.append(tracemalloc.is_tracing())
        if tracemalloc.is_tracing():
            raise RuntimeError("memory run failed")
    with pytest.raises(RuntimeError, match="memory run failed"):
        measure(lambda: None, run, repeats=5, track_memory=True)
    assert seen == [False] * 6 + [True]
    assert not tracemalloc.is_tracing()


def test_benchmark_preserves_five_raw_samples_and_unimplemented_status():
    frame = run_experiment("E1", [5], repeats=5)
    baseline = frame.loc[frame["implementasi"] == "Sorted list"].iloc[0]
    samples = json.loads(baseline["samples_ms"])
    assert len(samples) == 5
    assert baseline["waktu_ms"] == sorted(samples)[2]
    assert baseline["statistik"] == "median" and baseline["seed"] == 42
    heap = frame.loc[frame["implementasi"] == "Max-Heap"].iloc[0]
    if "belum diimplementasi" in heap["catatan"]:
        assert heap["waktu_ms"] != heap["waktu_ms"]  # NaN, bukan waktu 0
    with pytest.raises(ValueError, match="5 pengulangan"):
        run_experiment("E1", [5], repeats=3)


def test_delivery_uses_actual_order_coordinates_and_rejects_mixed_batches():
    restaurant = Restaurant("R1", "Test", 4.5, 0, (0.0, 0.0))
    order = Order("O1", "A", "R1", [], Priority.NORMAL, 0, (3.0, 4.0))
    service = DeliveryService()
    assert service.matrix_for_orders(restaurant, [order]) == [[0, 15], [15, 0]]
    assert service.matrix_for_orders(restaurant, []) == [[0]]
    with pytest.raises(ValueError, match="duplikat"):
        service.matrix_for_orders(restaurant, [order, order])
    order.restaurant_id = "R2"
    with pytest.raises(ValueError, match="restoran yang sama"):
        service.matrix_for_orders(restaurant, [order])
    with pytest.raises(ValueError, match="Kecepatan"):
        service.matrix_for_orders(restaurant, [], speed_kmh=float("nan"))

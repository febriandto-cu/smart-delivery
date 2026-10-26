"""Pemuatan seluruh CSV, validasi input dan tabel UI tanpa pemotongan."""
import csv
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.data.loader import load_csv_dataset
from src.services.search_service import SearchService


def test_load_csv_uses_every_row_and_validates_foreign_keys(csv_dataset):
    data, metadata = load_csv_dataset(csv_dataset)
    assert {name: len(rows) for name, rows in data.items()} == {"orders": 310, "restaurants": 205, "menus": 257}
    assert data["menus"][-1].menu_id == "M000256"
    assert data["restaurants"][-1].restaurant_id == "R000204"
    assert metadata["seed"] is None
    assert metadata["files"]["orders.csv"]["rows"] == 310
    assert len(metadata["files"]["orders.csv"]["sha256"]) == 64
    path = csv_dataset / "menus.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    rows[-1]["restaurant_id"] = "missing"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="missing"):
        load_csv_dataset(csv_dataset)


def test_no_limit_search_returns_all_ids_including_duplicate_names(csv_dataset):
    data, _ = load_csv_dataset(csv_dataset)
    service = SearchService()
    service.load(data["restaurants"], data["menus"])
    assert {r.restaurant_id for r in service.suggest_restaurants("", None)} == {r.restaurant_id for r in data["restaurants"]}
    assert {m.menu_id for m in service.suggest_menus("", None)} == {m.menu_id for m in data["menus"]}
    assert len(service.suggest_menus("", 10)) == 10  # API lama tetap kompatibel.


def test_evidence_search_and_queue_show_full_csv_tables(csv_dataset):
    root = Path(__file__).resolve().parents[1]
    app = AppTest.from_file(root / "app.py").run(timeout=30)
    assert app.session_state.dataset_metadata["source"] == "CSV lokal"
    app.switch_page("pages/8_Evidence_Dataset.py").run(timeout=30)
    assert not app.exception
    assert len(app.dataframe[0].value) == 310
    next(s for s in app.selectbox if s.label == "Lihat tabel").set_value("menus").run()
    assert len(app.dataframe[0].value) == 257
    app.switch_page("pages/2_Search.py").run()
    assert not app.exception
    assert any(len(frame.value) == 257 for frame in app.dataframe)
    assert any(len(frame.value) == 205 for frame in app.dataframe)
    app.switch_page("pages/1_Order_Management.py").run()
    assert app.radio(key="order_mode").value == "Dataset aplikasi"
    assert len(next(frame.value for frame in app.dataframe if "Urutan" in frame.value.columns)) == 310
    assert len(next(s for s in app.selectbox if s.label == "Restoran").options) == 205
    assert not app.exception


def test_missing_csv_does_not_silently_generate_data(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv_dataset(tmp_path)

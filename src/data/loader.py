"""Baca seluruh CSV generator sebagai entitas aplikasi; tanpa sampling."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import math
from pathlib import Path

from src.models import MenuItem, Order, OrderStatus, Priority, Restaurant

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CSV_FILES = ("orders.csv", "restaurants.csv", "menus.csv")


def csv_signature(directory: Path = DATA_DIR) -> tuple:
    """Signature perubahan file untuk invalidasi cache, bukan pemotongan data."""
    return tuple((name, (directory / name).stat().st_size, (directory / name).stat().st_mtime_ns)
                 for name in CSV_FILES)


def load_csv_dataset(directory: Path = DATA_DIR) -> tuple[dict, dict]:
    directory = Path(directory)
    requirements = {
        "restaurants.csv": {"restaurant_id", "name", "rating", "total_orders", "x", "y"},
        "menus.csv": {"menu_id", "restaurant_id", "name", "price"},
        "orders.csv": {"order_id", "customer_name", "restaurant_id", "items", "priority_level", "created_at", "x", "y"},
    }
    metadata = {"source": "CSV lokal", "directory": str(directory.resolve()), "seed": None,
        "seed_note": "Seed tidak disimpan pada format CSV sumber; tidak diasumsikan.",
        "loaded_at_utc": datetime.now(timezone.utc).isoformat(), "files": {}}

    def rows(filename):
        path = directory / filename
        metadata["files"][filename] = {"bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "rows": 0}
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = requirements[filename] - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"{filename}: kolom wajib tidak ada: {', '.join(sorted(missing))}")
            for row in reader:
                try:
                    if None in row or any(row.get(key) is None for key in requirements[filename]):
                        raise ValueError("Jumlah kolom tidak sesuai header")
                    yield row, reader.line_num
                    metadata["files"][filename]["rows"] += 1
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"{filename} baris {reader.line_num}: {exc}") from exc

    def number(row, key, filename, line, kind=float):
        try:
            value = kind(row[key])
            if not math.isfinite(value):
                raise ValueError("harus finite")
            return value
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{filename} baris {line}: {key} tidak valid ({row[key]!r})") from exc

    def unique_id(row, key, seen, filename, line):
        value = row[key].strip()
        if not value or value in seen:
            raise ValueError(f"{filename} baris {line}: {key} kosong/duplikat ({value!r})")
        seen.add(value)
        return value

    restaurants, menus, orders = [], [], []
    restaurant_ids = set()
    for row, line in rows("restaurants.csv"):
        filename = "restaurants.csv"
        oid = unique_id(row, "restaurant_id", restaurant_ids, filename, line)
        restaurants.append(Restaurant(oid, row["name"], number(row, "rating", filename, line),
            number(row, "total_orders", filename, line, int),
            (number(row, "x", filename, line), number(row, "y", filename, line))))
    for filename, id_key, target in [("menus.csv", "menu_id", menus), ("orders.csv", "order_id", orders)]:
        ids = set()
        for row, line in rows(filename):
            oid = unique_id(row, id_key, ids, filename, line)
            rid = row["restaurant_id"].strip()
            if rid not in restaurant_ids:
                raise ValueError(f"{filename} baris {line}: restoran {rid!r} tidak ada di restaurants.csv")
            if filename == "menus.csv":
                target.append(MenuItem(oid, rid, row["name"], number(row, "price", filename, line, int)))
            else:
                try:
                    raw = row["priority_level"].strip().upper()
                    level = Priority(int(raw)) if raw.isdigit() else Priority[raw]
                    status = OrderStatus(row.get("status", "pending").strip().lower())
                except (KeyError, ValueError) as exc:
                    raise ValueError(f"{filename} baris {line}: priority_level/status tidak valid") from exc
                target.append(Order(oid, row["customer_name"], rid,
                    row["items"].split(";") if row["items"] else [], level,
                    number(row, "created_at", filename, line),
                    (number(row, "x", filename, line), number(row, "y", filename, line)), status))
    if not restaurants or not orders or not menus:
        raise ValueError("Ketiga CSV harus memiliki setidaknya satu baris data")
    return {"orders": orders, "restaurants": restaurants, "menus": menus}, metadata

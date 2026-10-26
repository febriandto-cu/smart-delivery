import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest


@pytest.fixture
def csv_dataset(tmp_path, monkeypatch):
    """CSV temporer untuk tes UI, tanpa bergantung pada CSV lokal yang di-gitignore."""
    from src.data.generator import generate_menus, generate_orders, generate_restaurants, save_csv
    import src.ui
    restaurants = generate_restaurants(205, seed=7)
    menus = generate_menus(257, restaurants, seed=7)
    orders = generate_orders(310, restaurants, seed=7)
    save_csv(tmp_path / "restaurants.csv", [{"restaurant_id": r.restaurant_id, "name": r.name,
        "rating": r.rating, "total_orders": r.total_orders, "x": r.location[0], "y": r.location[1]}
        for r in restaurants])
    save_csv(tmp_path / "menus.csv", [vars(m) for m in menus])
    save_csv(tmp_path / "orders.csv", [{"order_id": o.order_id, "customer_name": o.customer_name,
        "restaurant_id": o.restaurant_id, "items": ";".join(o.items), "priority_level": o.priority_level.name,
        "created_at": o.created_at, "x": o.delivery_location[0], "y": o.delivery_location[1]} for o in orders])
    monkeypatch.setattr(src.ui, "DATA_DIR", tmp_path)
    return tmp_path

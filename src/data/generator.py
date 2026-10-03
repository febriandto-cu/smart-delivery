"""Generator dataset sintetis dengan seed tetap (Proposal Bagian 12).

Pemilik: QA & Performance Lead. Sudah jadi.

Pakai dari terminal:
    python -m src.data.generator --orders 100000 --restaurants 10000 --menus 50000
File CSV tersimpan di folder data/.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

from src.models import MenuItem, Order, Priority, Restaurant

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

_DISHES = ["Ayam Geprek", "Bakso", "Mie Ayam", "Nasi Goreng", "Sate", "Soto", "Martabak",
           "Seblak", "Pecel Lele", "Gado-Gado", "Ayam Bakar", "Nasi Padang", "Kopi Susu",
           "Bubur Ayam", "Rawon", "Gudeg", "Siomay", "Es Teh", "Roti Bakar", "Ketoprak"]
_OWNERS = ["Pak Kumis", "Bu Tini", "Mas Joko", "Cak Har", "Bang Udin", "Mbak Sri",
           "Kang Asep", "Bu Rudy", "Pak Gendut", "Mpok Ani", "Koh Ahong", "Uda Rizal"]
_PREFIX = ["Warung", "Kedai", "Depot", "Rumah Makan", "Dapur", ""]
_CUSTOMERS = ["Andi", "Budi", "Citra", "Dewi", "Eko", "Fitri", "Gilang", "Hana", "Indra",
              "Joko", "Kartika", "Lina", "Made", "Nanda", "Oki", "Putri", "Rizky", "Sari"]
_MENU_SUFFIX = ["Spesial", "Original", "Pedas", "Jumbo", "Komplit", "Keju", "Telur", ""]

# 10% Urgent, 30% High, 60% Normal
_PRIORITY_WEIGHTS = [(Priority.URGENT, 0.1), (Priority.HIGH, 0.3), (Priority.NORMAL, 0.6)]


def _point(rng: random.Random, size: float = 20.0) -> tuple[float, float]:
    return (round(rng.uniform(0, size), 3), round(rng.uniform(0, size), 3))


def generate_restaurants(n: int, seed: int = 42) -> list[Restaurant]:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        name = " ".join(p for p in (rng.choice(_PREFIX), rng.choice(_DISHES), rng.choice(_OWNERS)) if p)
        out.append(Restaurant(
            restaurant_id=f"R{i:06d}",
            name=name,
            rating=round(rng.uniform(3.0, 5.0), 1),
            total_orders=rng.randint(0, 20000),
            location=_point(rng),
        ))
    return out


def generate_menus(n: int, restaurants: list[Restaurant], seed: int = 42) -> list[MenuItem]:
    rng = random.Random(seed + 1)
    out = []
    for i in range(n):
        name = " ".join(p for p in (rng.choice(_DISHES), rng.choice(_MENU_SUFFIX)) if p)
        out.append(MenuItem(
            menu_id=f"M{i:06d}",
            restaurant_id=rng.choice(restaurants).restaurant_id,
            name=name,
            price=rng.randrange(8000, 85000, 500),
        ))
    return out


def generate_orders(n: int, restaurants: list[Restaurant], seed: int = 42) -> list[Order]:
    rng = random.Random(seed + 2)
    levels, weights = zip(*_PRIORITY_WEIGHTS)
    out = []
    for i in range(n):
        out.append(Order(
            order_id=f"ORD-{i:07d}",
            customer_name=rng.choice(_CUSTOMERS),
            restaurant_id=rng.choice(restaurants).restaurant_id,
            items=[rng.choice(_DISHES) for _ in range(rng.randint(1, 4))],
            priority_level=rng.choices(levels, weights)[0],
            created_at=round(rng.uniform(0, 24 * 60), 2),
            delivery_location=_point(rng),
        ))
    return out


def generate_distance_matrix(n_customers: int, seed: int = 42, speed_kmh: float = 20.0) -> list[list[float]]:
    """Matriks waktu tempuh (menit) simetris untuk restoran (titik 0) + n customer."""
    rng = random.Random(seed + 3)
    points = [_point(rng, 10.0) for _ in range(n_customers + 1)]
    minutes_per_km = 60.0 / speed_kmh
    return [[round(math.dist(a, b) * minutes_per_km, 1) for b in points] for a in points]


def save_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dataset sintetis Smart Delivery.")
    parser.add_argument("--orders", type=int, default=10000)
    parser.add_argument("--restaurants", type=int, default=1000)
    parser.add_argument("--menus", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    restaurants = generate_restaurants(args.restaurants, args.seed)
    menus = generate_menus(args.menus, restaurants, args.seed)
    orders = generate_orders(args.orders, restaurants, args.seed)

    save_csv(DATA_DIR / "restaurants.csv", [
        {"restaurant_id": r.restaurant_id, "name": r.name, "rating": r.rating,
         "total_orders": r.total_orders, "x": r.location[0], "y": r.location[1]} for r in restaurants])
    save_csv(DATA_DIR / "menus.csv", [vars(m) for m in menus])
    save_csv(DATA_DIR / "orders.csv", [
        {"order_id": o.order_id, "customer_name": o.customer_name, "restaurant_id": o.restaurant_id,
         "items": ";".join(o.items), "priority_level": o.priority_level.name,
         "created_at": o.created_at, "x": o.delivery_location[0], "y": o.delivery_location[1]}
        for o in orders])
    print(f"Tersimpan di {DATA_DIR}: {len(orders)} order, {len(restaurants)} restoran, {len(menus)} menu.")


if __name__ == "__main__":
    main()

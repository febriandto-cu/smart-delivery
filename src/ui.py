"""Helper Streamlit bersama untuk semua halaman. Pemilik: System Architect."""
from __future__ import annotations

import streamlit as st

from src.data.generator import generate_menus, generate_orders, generate_restaurants
from src.services.delivery_service import DeliveryService
from src.services.order_service import OrderService
from src.services.ranking_service import RankingService
from src.services.search_service import SearchService

DEFAULT_SIZES = {"orders": 1000, "restaurants": 500, "menus": 2000}


def build_services(orders: int, restaurants: int, menus: int, seed: int = 42) -> None:
    """Bangkitkan data lalu muat ke setiap service; modul yang belum jadi dicatat."""
    rest = generate_restaurants(restaurants, seed)
    data = {"restaurants": rest,
            "menus": generate_menus(menus, rest, seed),
            "orders": generate_orders(orders, rest, seed)}
    services = {"order": OrderService(), "search": SearchService(),
                "ranking": RankingService(), "delivery": DeliveryService()}
    errors = {}
    loaders = {"order": lambda: services["order"].load(data["orders"]),
               "search": lambda: services["search"].load(data["restaurants"], data["menus"]),
               "ranking": lambda: services["ranking"].load(data["restaurants"])}
    for key, load in loaders.items():
        try:
            load()
            errors[key] = None
        except NotImplementedError as e:
            errors[key] = str(e)
    st.session_state.update(data=data, services=services, service_errors=errors)


def get_services() -> tuple[dict, dict, dict]:
    if "services" not in st.session_state:
        build_services(**DEFAULT_SIZES)
    ss = st.session_state
    return ss.services, ss.service_errors, ss.data


def not_ready(module: str, detail: str) -> None:
    st.info(f"Fitur ini aktif setelah modul **{module}** selesai diimplementasi.\n\n`{detail}`")


def try_call(module: str, fn, *args, **kwargs):
    """Panggil fn; jika modul belum jadi tampilkan pesan dan return (False, None)."""
    try:
        return True, fn(*args, **kwargs)
    except NotImplementedError as e:
        not_ready(module, str(e))
        return False, None

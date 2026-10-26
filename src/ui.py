"""Helper Streamlit bersama untuk semua halaman. Pemilik: System Architect."""
from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from src.data.generator import generate_menus, generate_orders, generate_restaurants
from src.data.loader import DATA_DIR, csv_signature, load_csv_dataset
from src.services.delivery_service import DeliveryService
from src.services.order_service import OrderService
from src.services.ranking_service import RankingService
from src.services.search_service import SearchService

DEFAULT_SIZES = {"orders": 1000, "restaurants": 500, "menus": 2000}
SERVICE_VERSION = 3


def build_services(orders: int, restaurants: int, menus: int, seed: int = 42) -> None:
    """Bangkitkan data lalu muat ke setiap service; modul yang belum jadi dicatat."""
    rest = generate_restaurants(restaurants, seed)
    data = {"restaurants": rest,
            "menus": generate_menus(menus, rest, seed),
            "orders": generate_orders(orders, rest, seed)}
    _install_services(data, {"source": "Generator manual", "seed": seed, "requested_sizes": {
        "orders": orders, "restaurants": restaurants, "menus": menus},
        "generated_at_utc": datetime.now(timezone.utc).isoformat(), "generator": "src/data/generator.py"})


def _install_services(data: dict, metadata: dict, signature: tuple | None = None) -> None:
    for key in ("operational_events", "operational_notice"):
        st.session_state.pop(key, None)
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
    st.session_state.update(data=data, services=services, service_errors=errors,
                            service_version=SERVICE_VERSION,
                            dataset_metadata=metadata, csv_signature=signature)


@st.cache_data(show_spinner=False)
def _cached_csv(directory: str, signature: tuple) -> tuple[dict, dict]:
    from pathlib import Path
    return load_csv_dataset(Path(directory))


def reload_csv_services() -> None:
    signature = csv_signature(DATA_DIR)
    data, metadata = _cached_csv(str(DATA_DIR), signature)
    _install_services(data, metadata, signature)


def get_services() -> tuple[dict, dict, dict]:
    try:
        signature = csv_signature(DATA_DIR)
        if ("services" not in st.session_state or st.session_state.get("service_version") != SERVICE_VERSION
                or st.session_state.get("csv_signature") != signature):
            with st.spinner("Memuat seluruh CSV dan membangun indeks..."):
                reload_csv_services()
    except (OSError, ValueError) as exc:
        st.error(f"Dataset CSV tidak dapat dimuat: {exc}")
        st.info("Pastikan data/orders.csv, data/restaurants.csv dan data/menus.csv tersedia dan valid. "
                "Perbaiki CSV lalu muat ulang halaman. Aplikasi tidak menggantinya dengan data acak.")
        st.stop()
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

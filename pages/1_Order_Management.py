"""Order Management: Hash Table + Priority Queue (FR-01 s.d. FR-04).

Pemilik halaman: Business Analyst & Heap & PQ Engineer.
"""
import time

import pandas as pd
import streamlit as st

from src.models import Order, Priority
from src.ui import get_services, not_ready, try_call

st.set_page_config(page_title="Order Management", layout="wide")
st.title("Order Management")

services, errors, data = get_services()
orders = services["order"]
if errors["order"]:
    not_ready("Hash Table / Heap", errors["order"])
    st.stop()

left, right = st.columns(2)

with left:
    st.subheader("Tambah order")
    with st.form("add_order", clear_on_submit=True):
        customer = st.text_input("Nama customer", "Pelanggan Baru")
        restaurant = st.selectbox("Restoran", data["restaurants"][:200],
                                  format_func=lambda r: f"{r.name} ({r.restaurant_id})")
        level = st.radio("Prioritas", list(Priority), format_func=lambda p: p.name.title(),
                         horizontal=True, index=2)
        if st.form_submit_button("Tambah order"):
            new_id = f"ORD-N{int(time.time() * 1000) % 10**9:09d}"
            order = Order(new_id, customer, restaurant.restaurant_id, ["Menu pilihan"],
                          level, created_at=time.time() / 60 % (24 * 60),
                          delivery_location=(5.0, 5.0))
            ok, _ = try_call("Hash Table / Heap", orders.add_order, order)
            if ok:
                st.success(f"Order {new_id} ditambahkan dengan prioritas {level.name.title()}.")

with right:
    st.subheader("Order berikutnya")
    ok, nxt = try_call("Heap", orders.next_order)
    if ok and nxt:
        st.metric(nxt.order_id, nxt.priority_level.name.title(),
                  f"masuk menit ke-{nxt.created_at:.0f}", delta_color="off")
        if st.button("Proses order ini"):
            ok, done = try_call("Heap", orders.dispatch)
            if ok and done:
                st.success(f"{done.order_id} sedang diproses.")
                st.rerun()
    elif ok:
        st.write("Tidak ada order yang menunggu.")

    st.subheader("Batalkan order")
    cancel_id = st.text_input("order_id yang dibatalkan")
    if st.button("Batalkan") and cancel_id:
        ok, res = try_call("Hash Table", orders.cancel_order, cancel_id.strip())
        if ok:
            (st.success if res else st.error)(
                "Order dibatalkan." if res else "Order tidak ditemukan atau sudah diproses.")

st.subheader("Contoh data order")
st.dataframe(pd.DataFrame([{
    "order_id": o.order_id, "prioritas": o.priority_level.name.title(),
    "menit_masuk": o.created_at, "status": o.status.value} for o in data["orders"][:50]]),
    hide_index=True, width="stretch")

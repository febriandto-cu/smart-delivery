"""Beranda: ringkasan sistem dan status implementasi tiap modul.

Jalankan: streamlit run app.py
"""
import pandas as pd
import streamlit as st

from src.status import module_status
from src.ui import DEFAULT_SIZES, build_services, get_services

st.set_page_config(page_title="Smart Delivery & Order Optimization", layout="wide")

st.title("Smart Delivery & Order Optimization")
st.caption("Group 1 · Data Structure and Algorithm · 2026/2027")

statuses = module_status()
ready = sum(s["Status"] == "Siap" for s in statuses)
st.subheader(f"{ready} dari {len(statuses)} modul siap")
st.progress(ready / len(statuses))
st.dataframe(pd.DataFrame(statuses), hide_index=True, width="stretch")
st.caption("Status diperiksa dengan uji kecil setiap kali halaman dimuat. "
           "Uji lengkap: jalankan `pytest` dari terminal.")

st.subheader("Data yang dimuat")
services, errors, data = get_services()
c1, c2, c3 = st.columns(3)
c1.metric("Order", f"{len(data['orders']):,}".replace(",", "."))
c2.metric("Restoran", f"{len(data['restaurants']):,}".replace(",", "."))
c3.metric("Menu", f"{len(data['menus']):,}".replace(",", "."))

with st.form("reload"):
    st.write("Bangkitkan ulang dataset sintetis (seed tetap, hasil selalu sama).")
    a, b, c, d = st.columns(4)
    n_orders = a.number_input("Order", 10, 200_000, DEFAULT_SIZES["orders"], step=1000)
    n_rest = b.number_input("Restoran", 10, 50_000, DEFAULT_SIZES["restaurants"], step=500)
    n_menus = c.number_input("Menu", 10, 200_000, DEFAULT_SIZES["menus"], step=1000)
    seed = d.number_input("Seed", 0, 9999, 42)
    if st.form_submit_button("Muat ulang data"):
        build_services(int(n_orders), int(n_rest), int(n_menus), int(seed))
        st.rerun()

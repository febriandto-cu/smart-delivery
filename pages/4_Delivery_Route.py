"""Delivery Route: DP Held-Karp vs brute force (FR-15, FR-16).

Pemilik halaman: Dynamic Programming Engineer.
"""
import pandas as pd
import streamlit as st

from src.services.delivery_service import BRUTE_FORCE_LIMIT
from src.ui import get_services, try_call

st.set_page_config(page_title="Delivery Route", layout="wide")
st.title("Delivery Route")
st.write("**Bagian M Febri:** state DP, rute optimal dan perbandingan dengan brute force.")

services, _, data = get_services()
delivery = services["delivery"]

mode = st.radio("Sumber titik antar", ["Order dari dataset bersama", "Peta sintetis untuk eksperimen"])
if mode == "Order dari dataset bersama":
    grouped = {}
    for order in data["orders"]:
        if order.status.value in {"pending", "processing"}:
            grouped.setdefault(order.restaurant_id, []).append(order)
    available = [r for r in data["restaurants"] if r.restaurant_id in grouped]
    if not available:
        st.info("Belum ada order aktif dalam dataset. Muat ulang data dari Beranda.")
        st.stop()
    restaurant = st.selectbox("Restoran asal", available,
        format_func=lambda r: f"{r.name} ({r.restaurant_id}) — {len(grouped[r.restaurant_id])} order")
    options = grouped[restaurant.restaurant_id]
    selected = st.multiselect("Order dalam batch (maksimal 15)", options,
        default=options[:min(6, len(options))], format_func=lambda o: o.order_id,
        max_selections=15)
    if not selected:
        st.info("Pilih minimal satu order untuk dihitung rutenya.")
        st.stop()
    n = len(selected)
    dist = delivery.matrix_for_orders(restaurant, selected)
    labels = [restaurant.restaurant_id, *(o.order_id for o in selected)]
    st.caption("Titik 0 adalah koordinat restoran; titik berikutnya mengikuti urutan order yang dipilih. "
               "Waktu Euclidean pada kecepatan tetap 20 km/jam; pemilihan ini belum melakukan dispatch.")
    st.dataframe(pd.DataFrame({"titik": range(n + 1), "id": labels}), hide_index=True)
else:
    c1, c2 = st.columns(2)
    n = c1.slider("Jumlah customer dalam satu batch kurir", 2, 15, 6)
    seed = c2.number_input("Seed peta", 0, 9999, 42)
    dist = delivery.make_matrix(n, int(seed))
    labels = ["Restoran", *(f"C{i}" for i in range(1, n + 1))]

with st.expander("Matriks waktu tempuh (menit), titik 0 = restoran"):
    st.dataframe(pd.DataFrame(dist), width="stretch")

ok, dp = try_call("Dynamic Programming", delivery.optimize, dist)
if ok:
    st.subheader("Rute optimal (Held-Karp)")
    st.write(" → ".join(labels[p] for p in dp["route"]))
    st.metric("Total waktu", f"{dp['cost']:.1f} menit", f"{dp['ms']:.2f} ms komputasi",
              delta_color="off")

st.subheader("Pembanding brute force")
bf = delivery.brute_force(dist)
if bf is None:
    st.write(f"Brute force dilewati untuk n > {BRUTE_FORCE_LIMIT} karena {n}! urutan terlalu banyak.")
else:
    st.write(f"Total waktu {bf['cost']:.1f} menit, {bf['ms']:.2f} ms komputasi.")
    if ok:
        same = abs(bf["cost"] - dp["cost"]) < 1e-9
        (st.success if same else st.error)(
            "Hasil DP sama dengan brute force." if same else "Hasil DP berbeda dari brute force!")

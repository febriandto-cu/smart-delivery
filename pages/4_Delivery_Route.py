"""Delivery Route: DP Held-Karp vs brute force (FR-15, FR-16).

Pemilik halaman: Dynamic Programming Engineer.
"""
import pandas as pd
import streamlit as st

from src.services.delivery_service import BRUTE_FORCE_LIMIT
from src.ui import get_services, try_call

st.set_page_config(page_title="Delivery Route", layout="wide")
st.title("Delivery Route")

services, _, _ = get_services()
delivery = services["delivery"]

c1, c2 = st.columns(2)
n = c1.slider("Jumlah customer dalam satu batch kurir", 2, 15, 6)
seed = c2.number_input("Seed peta", 0, 9999, 42)
dist = delivery.make_matrix(n, int(seed))

with st.expander("Matriks waktu tempuh (menit), titik 0 = restoran"):
    st.dataframe(pd.DataFrame(dist), width="stretch")

ok, dp = try_call("Dynamic Programming", delivery.optimize, dist)
if ok:
    st.subheader("Rute optimal (Held-Karp)")
    st.write(" → ".join("Restoran" if p == 0 else f"C{p}" for p in dp["route"]))
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

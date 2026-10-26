"""Restaurant Ranking: AVL Tree (FR-11 s.d. FR-14).

Pemilik halaman: AVL Tree Engineer.
"""
import math

import pandas as pd
import streamlit as st

from src.ui import get_services, not_ready, try_call

st.set_page_config(page_title="Ranking", layout="wide")
st.title("Restaurant Ranking")
st.write("**Bagian Febri Andri:** ranking, pembaruan rating dan rotasi AVL Tree.")

services, errors, data = get_services()
if errors["ranking"]:
    not_ready("AVL Tree", errors["ranking"])
    st.stop()

ranking = services["ranking"]
tree = ranking.tree
n = len(tree)
c1, c2, c3 = st.columns(3)
c1.metric("Restoran di pohon", n)
c2.metric("Tinggi AVL", tree.height(tree.root))
c3.metric("Batas teoritis 1,44·log₂(n)", f"{1.44 * math.log2(max(n, 2)):.1f}")

left, right = st.columns(2)
with left:
    k = st.slider("Top-k", 1, 50, 10)
    ok, top = try_call("AVL Tree", ranking.top, k)
    if ok:
        st.dataframe(pd.DataFrame([{"nama": r.name, "rating": r.rating, "id": r.restaurant_id}
                                   for r in top]), hide_index=True, width="stretch")
with right:
    min_rating = st.slider("Rating minimal", 3.0, 5.0, 4.8, 0.1)
    ok, res = try_call("AVL Tree", ranking.above, min_rating)
    if ok:
        st.write(f"{len(res)} restoran dengan rating ≥ {min_rating}")

st.subheader("Perbarui rating")
rest = st.selectbox("Restoran", data["restaurants"][:200],
                    format_func=lambda r: f"{r.name} ({r.rating})")
new_rating = st.number_input("Rating baru", 1.0, 5.0, 4.5, 0.1)
if st.button("Simpan rating"):
    ok, _ = try_call("AVL Tree", ranking.update_rating, rest, round(new_rating, 1))
    if ok:
        st.success("Rating diperbarui (delete lalu reinsert).")

st.subheader("Log rotasi terakhir")
st.code("\n".join(tree.rotation_log[-20:]) or "Belum ada rotasi tercatat.")

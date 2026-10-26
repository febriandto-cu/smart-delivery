"""Performance Lab: eksperimen E1-E5 (FR-17).

Pemilik halaman: QA & Performance Lead.
"""
import altair as alt
import streamlit as st

from src.services.benchmark_service import BASELINE_LIMIT, EXPERIMENTS, run_experiment

st.set_page_config(page_title="Performance Lab", layout="wide")
st.title("Performance Lab")
st.write("**Bagian Daffa:** kompleksitas, pengujian dan eksperimen. "
         "Setiap pemilik modul tetap mempelajari hasil pengujian bagiannya.")

exp = st.selectbox("Eksperimen", list(EXPERIMENTS), format_func=lambda e: f"{e} · {EXPERIMENTS[e]}")
if exp == "E5":
    sizes = st.multiselect("Jumlah customer (n)", list(range(4, 16)), [4, 6, 8, 9, 10, 12])
else:
    sizes = st.multiselect("Ukuran data (n)", [1_000, 5_000, 10_000, 50_000, 100_000],
                           [1_000, 10_000, 50_000, 100_000])
repeats = st.slider("Pengulangan per titik (median)", 5, 15, 5)
st.caption("Satu warm-up; minimal lima sampel waktu. Peak memory diukur pada run terpisah. "
           "CSV menyimpan sampel mentah, seed, dan versi lingkungan. "
           "E1–E5 masih cakupan UTS; eksperimen tambahan direncanakan di UAS Workspace.")
log_scale = st.checkbox("Sumbu waktu skala log", value=exp == "E5")
st.caption(f"Baseline dilewati untuk n > {BASELINE_LIMIT[exp]:,} karena terlalu lama.".replace(",", "."))

if st.button("Jalankan eksperimen", type="primary") and sizes:
    with st.spinner("Mengukur..."):
        df = run_experiment(exp, sorted(sizes), repeats)
    st.session_state[f"result_{exp}"] = df

df = st.session_state.get(f"result_{exp}")
if df is not None:
    plot = df.dropna(subset=["waktu_ms"])
    if not plot.empty:
        chart = alt.Chart(plot).mark_line(point=True).encode(
            x=alt.X("n:Q", title="Ukuran input (n)"),
            y=alt.Y("waktu_ms:Q", title="Waktu median (ms)",
                    scale=alt.Scale(type="log") if log_scale else alt.Scale()),
            color=alt.Color("implementasi:N", title=None),
            tooltip=["implementasi", "n", "waktu_ms"])
        st.altair_chart(chart, width="stretch")
    st.dataframe(df, hide_index=True, width="stretch")
    st.download_button("Unduh hasil (CSV)", df.to_csv(index=False), f"{exp}_hasil.csv", "text/csv")

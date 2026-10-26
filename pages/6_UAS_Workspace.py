"""Peta tugas dan bukti UAS untuk sembilan anggota; tidak mengklaim sesi selesai."""
import pandas as pd
import streamlit as st

from src.services.uas_service import session_checklist
from src.uas import SESSIONS, PRESENTATION
from src.presentation_ui import member_cards

st.set_page_config(page_title="UAS Workspace", layout="wide")
st.title("UAS Workspace — Kelompok 1")
st.caption("Sumber: Guideline UAS hlm. 4–15; pembagian mengikuti pemateri teknis UTS.")
st.info("Target tim: seluruh sesi Level 2, lalu Level 3 sesuai bukti. "
        "Audit file di bawah belum membuktikan correctness atau pencapaian level.")

team_tab, rubric_tab, evidence_tab = st.tabs(["Pembagian tim", "Target 12 sesi", "Checklist bukti"])
with team_tab:
    st.subheader("Pilih bagian individu")
    member_cards()
    st.subheader("Urutan pemateri sesuai UTS")
    presentation = pd.DataFrame(PRESENTATION, columns=["Pemateri", "Slide UTS", "Materi", "Durasi (menit)"])
    st.dataframe(presentation,
                 hide_index=True, width="stretch")
    st.write(f"Total durasi acuan UTS: {presentation['Durasi (menit)'].sum():g} menit.")
    st.caption("Peran mengikuti tabel presentasi UTS. Slide dan durasi UAS disesuaikan ketentuan dosen.")
    st.info("Pemilik tambahan S6 dan S9–S13 serta reviewer belum ditentukan. "
            "Kebutuhan algoritma UAS tetap tercatat terpisah dari pembagian presentasi.")
with rubric_tab:
    chosen = st.selectbox("Sesi", SESSIONS, format_func=lambda s: f"{s.code} · {s.title}")
    st.write(f"**Pemilik:** {chosen.owner} · **Reviewer:** {chosen.reviewer} · **Bobot:** {chosen.weight}")
    for label, content in [("Level 1", chosen.minimum), ("Level 2", chosen.standard),
                           ("Level 3", chosen.excellent), ("Klaim yang diuji", chosen.claim),
                           ("Eksperimen", chosen.experiment)]:
        st.write(f"**{label}:** {content}")
    st.code("\n".join(chosen.files + chosen.tests), language="text")
    st.write(f"Minimal {chosen.min_tests} test case; setiap operasi dan invarian tetap perlu diuji.")
with evidence_tab:
    frame = pd.DataFrame(session_checklist())
    st.dataframe(frame, hide_index=True, width="stretch")
    st.download_button("Unduh checklist CSV", frame.to_csv(index=False).encode("utf-8-sig"),
                       "uas_checklist.csv", "text/csv")
    st.caption("Jumlah artefak adalah jumlah file nonkosong, belum verifikasi isi. "
               "Simpan di docs/evidence/Sxx/{visual,screenshot,table,benchmark,slides,interpretation}/. "
               "Minimal 2 gambar dan 1 tabel tiap sesi; grafik minimal 8 sesi.")
st.warning("Panduan memuat perbedaan tanggal (27/31 Oktober), durasi (30/40 menit), "
           "dan jumlah halaman (15/30). Catatan sumber dan rencana konservatif ada di docs/UAS_PLAN.md.")

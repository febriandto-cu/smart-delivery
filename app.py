"""Beranda: ringkasan sistem dan status implementasi tiap modul.

Jalankan: streamlit run app.py
"""
import pandas as pd
import streamlit as st

from src.status import module_status
from src.services.uas_service import session_checklist
from src.ui import get_services, reload_csv_services
from src.presentation_ui import member_cards

st.set_page_config(page_title="Smart Delivery & Order Optimization", layout="wide")

st.title("Smart Delivery & Order Optimization")
st.caption("Group 1 · Data Structure and Algorithm · 2026/2027")

st.subheader("Mulai dari bagianmu")
st.write("Pilih nama anggota. Setiap bagian berisi tugas, urutan presentasi, demo yang bisa dicoba, "
         "file terkait, dan bukti yang perlu disiapkan.")
member_cards()
st.info("Peran mengikuti pembagian UTS kalian. Tambahan sesi UAS tetap dicatat di UAS Workspace; "
        "pemilik tambahan belum ditentukan. Demo fondasi yang berjalan belum berarti seluruh UAS selesai.")
st.page_link("pages/8_Evidence_Dataset.py", label="Evidence & Dataset — lihat data, hasil algoritma dan unduh bukti", icon="📊")
with st.expander("Status teknis dan cakupan 12 sesi UAS"):
    st.dataframe(pd.DataFrame(session_checklist())[["Sesi", "Topik", "Pemilik", "Kode", "TODO"]],
                 hide_index=True, width="stretch")
    st.write("Uji singkat lima modul fondasi UTS")
    st.dataframe(pd.DataFrame(module_status()), hide_index=True, width="stretch")
    st.caption("Status Siap di tabel ini hanya berarti uji kecil lulus; bukan seluruh syarat UAS terpenuhi.")

st.subheader("Dataset bersama untuk demo aplikasi")
services, errors, data = get_services()
c1, c2, c3 = st.columns(3)
c1.metric("Order", f"{len(data['orders']):,}".replace(",", "."))
c2.metric("Restoran", f"{len(data['restaurants']):,}".replace(",", "."))
c3.metric("Menu", f"{len(data['menus']):,}".replace(",", "."))

st.caption("Sumber utama: data/orders.csv, data/restaurants.csv dan data/menus.csv. "
           "Seluruh baris dimuat dan dipakai oleh service. Perubahan selama demo tersimpan di session, "
           "tidak menimpa CSV sumber.")
if st.button("Muat ulang seluruh CSV"):
    reload_csv_services()
    st.rerun()
st.caption("Muat ulang mengembalikan session aplikasi ke isi CSV. File CSV yang berubah juga dimuat ulang otomatis.")

"""Panduan presentasi dan demo yang dipilih berdasarkan nama anggota."""
import streamlit as st

from src.presentation import GUIDES
from src.presentation_ui import render_member

st.set_page_config(page_title="Bagian Individu", layout="wide")
st.title("Bagian Individu")
st.write("Pilih nama untuk melihat tugas, urutan presentasi, demo, file dan bukti bagianmu.")
names = [guide.name for guide in GUIDES]
selected = st.session_state.get("selected_member", names[0])
if selected not in names:
    st.session_state.selected_member = names[0]
name = st.selectbox("Nama anggota", names, key="selected_member")
render_member(name)
st.divider()
st.caption("Peran utama mengikuti tabel UTS yang disepakati. Tambahan S6 dan S9–S13 "
           "tetap membutuhkan pembagian terpisah; lihat UAS Workspace.")

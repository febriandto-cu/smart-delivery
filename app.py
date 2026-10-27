"""Entrypoint navigasi. Beranda lama disimpan tanpa menu di src/home.py."""
import streamlit as st

st.set_page_config(page_title="Smart Delivery & Order Optimization", layout="wide")

page = st.navigation([
    st.Page("pages/1_Order_Management.py", title="Order Management", url_path="Order_Management", default=True),
    st.Page("pages/2_Search.py", title="Search", url_path="Search"),
    st.Page("pages/3_Ranking.py", title="Ranking", url_path="Ranking"),
    st.Page("pages/4_Delivery_Route.py", title="Delivery Route", url_path="Delivery_Route"),
    st.Page("pages/5_Performance_Lab.py", title="Performance Lab", url_path="Performance_Lab"),
    st.Page("pages/6_UAS_Workspace.py", title="UAS Workspace", url_path="UAS_Workspace", visibility="hidden"),
    st.Page("pages/7_Bagian_Individu.py", title="Bagian Individu", url_path="Bagian_Individu", visibility="hidden"),
    st.Page("pages/8_Evidence_Dataset.py", title="Evidence & Dataset", url_path="Evidence_Dataset"),
])
page.run()

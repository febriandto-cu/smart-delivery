"""Search: Hash Table untuk order, Trie untuk restoran dan menu (FR-07 s.d. FR-10).

Pemilik halaman: Hash Table Engineer & Trie Engineer.
"""
import pandas as pd
import streamlit as st

from src.ui import get_services, not_ready, try_call

st.set_page_config(page_title="Search", layout="wide")
st.title("Search")

services, errors, data = get_services()
tab_order, tab_rest, tab_menu = st.tabs(["Order (Hash Table)", "Restoran (Trie)", "Menu (Trie)"])

with tab_order:
    if errors["order"]:
        not_ready("Hash Table / Heap", errors["order"])
    else:
        table = services["order"].table
        order_id = st.text_input("order_id", data["orders"][0].order_id)
        ok, order = try_call("Hash Table", table.get, order_id.strip())
        if ok:
            if order:
                st.json({"order_id": order.order_id, "customer": order.customer_name,
                         "restoran": order.restaurant_id, "items": order.items,
                         "prioritas": order.priority_level.name, "status": order.status.value})
            else:
                st.warning("Order tidak ditemukan.")
        st.caption("Statistik Hash Table")
        st.dataframe(pd.DataFrame([table.stats()]), hide_index=True)

with tab_rest:
    if errors["search"]:
        not_ready("Trie", errors["search"])
    else:
        prefix = st.text_input("Ketik nama restoran", "ba")
        ok, res = try_call("Trie", services["search"].suggest_restaurants, prefix, 10)
        if ok:
            st.dataframe(pd.DataFrame([{"id": r.restaurant_id, "nama": r.name, "rating": r.rating}
                                       for r in res]), hide_index=True, width="stretch")

with tab_menu:
    if errors["search"]:
        not_ready("Trie", errors["search"])
    else:
        prefix = st.text_input("Ketik nama menu", "ayam")
        ok, res = try_call("Trie", services["search"].suggest_menus, prefix, 10)
        if ok:
            st.dataframe(pd.DataFrame([{"id": m.menu_id, "menu": m.name, "harga": m.price,
                                        "restoran": m.restaurant_id} for m in res]),
                         hide_index=True, width="stretch")

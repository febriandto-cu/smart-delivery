"""Dataset, input-output, dan paket bukti yang dapat diperiksa saat presentasi."""
import json

import pandas as pd
import streamlit as st

from src.presentation import FEATURE_MAPPING, GUIDES
from src.presentation_ui import heap_diagram
from src.services.evidence_service import collect_cases, dataset_frames, evidence_bundle, evidence_summary
from src.services.order_demo import create_demo, queue_preview, selection_reason
from src.ui import get_services, reload_csv_services

st.set_page_config(page_title="Evidence & Dataset", layout="wide")
st.title("Evidence & Dataset")
st.write("Tunjukkan data yang dipakai, cocokkan input dan hasil algoritma, lalu unduh bukti untuk laporan atau dosen.")

source = st.radio("Sumber dataset", ["Dataset aplikasi", "Demo presentasi"], horizontal=True, key="evidence_source")
services, errors, data = get_services()
is_demo = source == "Demo presentasi"
if is_demo:
    if "guided_demo_orders" in st.session_state:
        active_data = {"orders": st.session_state.guided_demo_orders}
        demo_service = st.session_state.guided_demo_service
        source_detail = "Snapshot demo presentasi yang sedang digunakan pada Order Management."
        events = st.session_state.get("guided_demo_events", [])
    else:
        demo_service, demo_orders = create_demo()
        active_data = {"orders": demo_orders}
        source_detail = "Contoh awal empat order; demo belum dijalankan pada session ini."
        events = []
    metadata = {"source": source, "description": source_detail, "seed": None,
                "generator": "src/services/order_demo.py:create_demo", "units": "menit, km, rupiah"}
else:
    active_data = data
    source_detail = "Seluruh data dari CSV lokal, sama dengan data aktif Order Management, Search, Ranking dan Delivery Route."
    events = st.session_state.get("operational_events", [])
    metadata = {**st.session_state.get("dataset_metadata", {}), "source": source,
                "description": source_detail, "units": "menit, km, rupiah"}

frames = dataset_frames(active_data)
cases = collect_cases()
benchmarks = {name: st.session_state[f"result_{name}"] for name in ["E1", "E2", "E3", "E4", "E5"]
              if f"result_{name}" in st.session_state}
st.caption(source_detail)
dataset_tab, cases_tab, history_tab, results_tab, export_tab = st.tabs([
    "Dataset & distribusi", "Bukti algoritma", "Riwayat demo", "Benchmark & log tes", "Unduh paket bukti"])

with dataset_tab:
    if not is_demo:
        if st.button("Muat ulang seluruh CSV"):
            reload_csv_services()
            st.rerun()
        st.caption("Muat ulang mengembalikan data session ke isi CSV sumber.")
    a, b, c = st.columns(3)
    a.metric("Order", len(frames["orders"]))
    b.metric("Restoran", len(frames["restaurants"]))
    c.metric("Menu", len(frames["menus"]))
    if is_demo:
        st.info("Demo hanya menyediakan order contoh. Daftar restoran dan menu tidak disalin dari dataset aplikasi.")
    else:
        seed = metadata.get("seed")
        st.caption(f"Seed generator: {seed if seed is not None else 'tidak disimpan di CSV sumber'}. "
                   "Data sintetis untuk simulasi, bukan transaksi nyata. Aksi pada aplikasi dapat mengubah snapshot ini.")
    selected = st.selectbox("Lihat tabel", [name for name, frame in frames.items() if not frame.empty],
                            format_func=lambda name: {"orders": "Order", "restaurants": "Restoran", "menus": "Menu"}[name])
    frame = frames[selected]
    st.dataframe(frame, hide_index=True, width="stretch")
    st.caption(f"Seluruh {len(frame):,} baris tersedia pada tabel. Gulir tabel untuk melihat baris lainnya; tidak ada sampling.")
    st.download_button("Unduh tabel lengkap (CSV)", frame.to_csv(index=False).encode("utf-8-sig"),
        f"{selected}_{'demo' if is_demo else 'aplikasi'}.csv", "text/csv")
    left, right = st.columns(2)
    orders = frames["orders"]
    with left:
        st.subheader("Distribusi prioritas order")
        counts = orders["priority"].value_counts().reindex(["URGENT", "HIGH", "NORMAL"], fill_value=0)
        st.bar_chart(counts.rename("Jumlah order"))
    with right:
        st.subheader("Status order saat ini")
        st.bar_chart(orders["status"].value_counts().rename("Jumlah order"))
    with st.expander("Arti kolom dan asal data"):
        st.write("**priority_level:** level data lama (Urgent=1, High=2, Normal=3). "
                 "**max_heap_score:** skor pemrosesan (Urgent=3, High=2, Normal=1).")
        st.write("**created_at_minutes:** menit sejak awal hari; **created_at_hhmm:** tampilan jam. "
                 "**delivery_x/y_km:** koordinat simulasi; **items_json:** daftar item. "
                 "**price_rupiah:** harga menu; **status:** pending/processing/done/cancelled.")
        st.json(metadata)

with cases_tab:
    passed = sum(c["passed"] for c in cases)
    st.subheader(f"{passed} dari {len(cases)} pemeriksaan contoh lulus")
    st.caption("Dihitung ulang menggunakan implementasi asli pada input kecil terpisah. "
               "Tidak mengubah order aktif, bukan hasil benchmark, dan bukan pengganti suite tes/rubrik UAS lengkap.")
    owner = st.selectbox("Bukti untuk anggota", ["Semua anggota", *(guide.name for guide in GUIDES)])
    filtered = cases if owner == "Semua anggota" else [case for case in cases if case["owner"] == owner]
    if not filtered:
        st.info("Bagian ini menggunakan bukti lintas modul: dataset, arsitektur, pemetaan fitur dan rekap pengujian. "
                "Pilih Semua anggota untuk melihat hasil algoritma.")
        st.dataframe(pd.DataFrame(FEATURE_MAPPING, columns=["Fitur", "Pemateri teknis", "Struktur", "Key", "Alasan"]),
                     hide_index=True, width="stretch")
    else:
        summary = evidence_summary(filtered)
        st.dataframe(summary, hide_index=True, width="stretch")
        chosen = st.selectbox("Lihat input dan hasil", filtered, format_func=lambda case: f"{case['id']} · {case['owner']}")
        st.write(f"**Klaim:** {chosen['claim']}")
        left, right = st.columns(2)
        with left:
            st.write("**Input yang dijalankan**")
            st.json(chosen["input"])
            st.write("**Hasil yang diharapkan**")
            st.json(chosen["expected"])
        with right:
            st.write("**Hasil aktual dari kode**")
            st.json(chosen["actual"])
            if chosen["passed"]:
                st.success("Hasil aktual sesuai hasil yang diharapkan pada input ini.")
            else:
                st.error(chosen["error"] or "Hasil aktual berbeda dari expected.")
        details = chosen["details"]
        if "initial_heap" in details:
            st.write("**Pohon Max-Heap sebelum pemrosesan**")
            st.graphviz_chart(heap_diagram(details["initial_heap"]))
            st.dataframe(pd.DataFrame(details["input_orders"]), hide_index=True, width="stretch")
        elif "buckets_before_delete" in details:
            st.write("**Bucket sebelum penghapusan ORD-5**")
            st.dataframe(pd.DataFrame(details["buckets_before_delete"]), hide_index=True, width="stretch")
            st.caption("max_load=100 hanya pada kasus ini untuk menjaga collision terlihat tanpa rehash.")
        elif "trace" in details:
            st.write("**Trace insert dan validasi AVL**")
            st.dataframe(pd.DataFrame(details["trace"]), hide_index=True, width="stretch")
            st.code("\n".join(details["rotation_log"]), language="text")
        elif "matrix" in details:
            st.write("**Matriks waktu (menit) dan rekonstruksi rute**")
            st.dataframe(pd.DataFrame(details["matrix"]), width="stretch")
            st.write(" → ".join("Restoran" if i == 0 else f"C{i}" for i in details["route"]))
        elif "prefix_path" in details:
            st.write("**Jalur prefix:** " + " → ".join(details["prefix_path"]))
            st.caption(f"{details['word_count']} kata unik, {details['node_count']} node pada Trie contoh.")
        st.download_button("Unduh hasil pemeriksaan (CSV)", summary.to_csv(index=False).encode("utf-8-sig"),
                           "algorithm-checks.csv", "text/csv")

with history_tab:
    st.write(f"**Sumber riwayat:** {source}. Aksi berasal dari session browser ini.")
    if events:
        st.dataframe(pd.DataFrame(events), hide_index=True, width="stretch")
    else:
        st.info("Belum ada aksi tercatat untuk sumber ini. Coba tambah, proses atau batal order pada Order Management.")
    if is_demo:
        preview = queue_preview(demo_service)
        st.write("**Antrean demo yang tersisa**")
        st.write(" → ".join(f"{o.customer_name} ({o.order_id})" for o in preview) or "Antrean kosong")
        st.caption(selection_reason(preview))
    st.page_link("pages/1_Order_Management.py", label="Buka demo dan jalankan beberapa aksi", icon="↗️")

with results_tab:
    st.subheader("Hasil Performance Lab pada session ini")
    if benchmarks:
        for name, result in benchmarks.items():
            with st.expander(f"{name} · {len(result)} baris hasil", expanded=True):
                st.dataframe(result, hide_index=True, width="stretch")
                st.download_button(f"Unduh {name} (CSV)", result.to_csv(index=False).encode("utf-8-sig"),
                                   f"{name}.csv", "text/csv")
    else:
        st.info("Belum ada benchmark di session ini. Jalankan eksperimen dari Performance Lab terlebih dahulu.")
    st.page_link("pages/5_Performance_Lab.py", label="Buka Performance Lab", icon="↗️")
    st.subheader("Log pengujian terakhir")
    if "presentation_test_result" in st.session_state:
        code, log = st.session_state.presentation_test_result
        (st.success if code == 0 else st.error)("Perintah tes terakhir berhasil." if code == 0 else "Perintah tes terakhir gagal.")
        st.code(log, language="text")
        st.caption("Log terakhir dari Bagian Individu Daffa; jalankan ulang setelah perubahan kode.")
    else:
        st.caption("Belum ada log tes. Pada Bagian Individu, pilih Daffa lalu klik Jalankan pengujian proyek.")

with export_tab:
    st.subheader("Simpan satu paket yang bisa diperiksa dosen")
    st.write("ZIP berisi tiga tabel CSV, metadata sumber/seed/jumlah data, delapan kasus input–expected–actual, "
             "serta checksum data. Riwayat aksi, hasil benchmark dan log tes ikut disertakan jika sudah tersedia.")
    st.caption("Paket ini snapshot saat disiapkan. Screenshot dan interpretasi laporan tetap perlu dibuat dari eksekusi nyata.")
    if st.button("Siapkan paket bukti ZIP", type="primary"):
        log = st.session_state.get("presentation_test_result", (None, ""))[1]
        st.session_state.evidence_export = {
            "source": source, "data": evidence_bundle(frames, metadata, cases, events, benchmarks, log)}
    export = st.session_state.get("evidence_export")
    if export and export["source"] == source:
        st.download_button("Unduh paket bukti ZIP", export["data"],
            "evidence_demo.zip" if is_demo else "evidence_aplikasi.zip", "application/zip")
        st.caption("Jika data atau hasil berubah, klik Siapkan paket bukti ZIP lagi agar snapshot diperbarui.")

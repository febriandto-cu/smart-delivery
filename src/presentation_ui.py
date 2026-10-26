"""UI bagian individu dan demo kecil dengan implementasi asli, bukan hasil contoh."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import streamlit as st

from src.presentation import FEATURE_MAPPING, GUIDES
from src.uas import PRESENTATION


def member_cards() -> None:
    for offset in range(0, len(GUIDES), 3):
        columns = st.columns(3)
        for column, guide in zip(columns, GUIDES[offset:offset + 3]):
            with column, st.container(border=True):
                st.subheader(guide.name)
                st.write(guide.role)
                if st.button("Buka bagian saya", key=f"member_{guide.name}", width="stretch"):
                    st.session_state["selected_member"] = guide.name
                    st.switch_page("pages/7_Bagian_Individu.py")


def heap_diagram(keys: list[tuple]) -> str:
    lines = ['digraph heap { node [shape=box, style="rounded,filled", fillcolor="#EEF2EE"];']
    for i, key in enumerate(keys):
        label = json.dumps(f"{key[-1]}\nSkor {key[0]} | menit {-key[1]:g}")
        lines.append(f"n{i} [label={label}];")
        if i:
            lines.append(f"n{(i - 1) // 2} -> n{i};")
    lines.append("}")
    return "\n".join(lines)


def _new_queue():
    from src.ds.heap import OrderPriorityQueue
    from src.models import Order, Priority
    queue = OrderPriorityQueue()
    queue.heap.trace_enabled = True
    for oid, level, minute in [("Normal-1", Priority.NORMAL, 470),
            ("Urgent-A", Priority.URGENT, 480), ("High-1", Priority.HIGH, 475),
            ("Urgent-B", Priority.URGENT, 480)]:
        queue.push(Order(oid, "Demo", "R-DEMO", [], level, minute, (0, 0)))
    return queue


def _heap_demo():
    from src.models import Order, Priority
    st.caption("Simulasi kecil khusus Max-Heap. Tidak mengubah order operasional atau membutuhkan Hash Table.")
    if "presentation_queue" not in st.session_state:
        st.session_state.presentation_queue = _new_queue()
        st.session_state.presentation_events = []
    queue = st.session_state.presentation_queue
    with st.form("heap_demo_add"):
        left, right = st.columns(2)
        level = left.selectbox("Prioritas order demo", list(Priority), format_func=lambda p: p.name.title())
        minute = right.number_input("Menit masuk order demo", min_value=0, value=480, step=1)
        if st.form_submit_button("Tambahkan ke Max-Heap"):
            oid = f"Demo-{queue._sequence + 1}"
            queue.push(Order(oid, "Demo", "R-DEMO", [], level, float(minute), (0, 0)))
            st.session_state.presentation_events.append({"aksi": "insert", "order_id": oid})
    first, second = st.columns(2)
    if first.button("Ambil order tertinggi", disabled=not len(queue)):
        oid = queue.pop()
        st.session_state.presentation_events.append({"aksi": "extract_max", "order_id": oid})
        st.success(f"Order yang diambil: {oid}")
    if second.button("Reset simulasi"):
        st.session_state.presentation_queue = _new_queue()
        st.session_state.presentation_events = []
        st.rerun()
    a, b, c = st.columns(3)
    a.metric("Order berikutnya", queue.peek() or "Kosong")
    b.metric("Panjang antrean", len(queue))
    c.metric("Heap valid", "Ya" if queue.heap.is_heap() else "Tidak")
    keys = queue.heap._data
    if keys:
        st.graphviz_chart(heap_diagram(keys))
        st.dataframe(pd.DataFrame([{"indeks array": i, "order_id": key[-1],
            "skor": key[0], "menit masuk": -key[1], "sequence": -key[2]}
            for i, key in enumerate(keys)]), hide_index=True, width="stretch")
    else:
        st.info("Antrean kosong. Tambahkan order baru atau reset simulasi.")
    st.caption("Array heap bukan daftar yang seluruhnya terurut. Parent harus >= anak. "
               "Urgent-A masuk sebelum Urgent-B pada menit sama, sehingga A keluar lebih dulu.")
    with st.expander("Log operasi dan pertukaran terakhir"):
        st.json({"operasi": st.session_state.presentation_events[-15:], "swap": queue.heap.trace[-15:]})


def _hash_demo():
    from src.ds.hash_table import HashTable
    st.caption("Tabel kecil manual untuk melihat collision; terpisah dari data operasional.")
    table = HashTable(capacity=5, max_load=100)
    for i in range(12):
        table.put(f"ORD-D{i:03d}", f"Customer {i}")
    query = st.text_input("ID order demo", "ORD-D003")
    value = table.get(query.strip())
    if value is None:
        st.warning("Order tidak ditemukan.")
    else:
        st.success(f"{query.strip()} → {value}; bucket {table.hash_function(query.strip())}")
    st.dataframe(pd.DataFrame([{"bucket": i, "jumlah key": len(bucket),
        "chain": " → ".join(k for k, _ in bucket)} for i, bucket in enumerate(table.buckets)]),
        hide_index=True, width="stretch")
    st.caption("Rehash dimatikan hanya pada contoh ini (max_load=100) agar collision terlihat. "
               "Tabel aplikasi memakai batas load factor 0,75.")


def _trie_demo():
    from src.ds.trie import Trie, normalize
    trie = Trie()
    for name, oid in [("Ayam Geprek", "R1"), ("Ayam Bakar", "R2"),
                       ("Bakso Pak Kumis", "R3"), ("Bakso Pak Kumis", "R4")]:
        trie.insert(name, oid)
    prefix = st.text_input("Prefix nama restoran demo", "ay")
    st.write("Jalur prefix:", " → ".join(["root", *normalize(prefix)]))
    results = trie.starts_with(prefix)
    st.dataframe(pd.DataFrame([{"nama": word, "ID restoran": ", ".join(ids)}
        for word, ids in results], columns=["nama", "ID restoran"]), hide_index=True, width="stretch")
    if not results:
        st.info("Tidak ada kata dengan prefix tersebut.")
    st.caption(f"{trie.word_count} kata unik, {trie.node_count} node. Nama sama dapat memiliki beberapa ID.")


def _avl_demo():
    from src.ds.avl import AVLTree
    choices = {"LL": [4.8, 4.5, 4.2], "RR": [4.2, 4.5, 4.8],
               "LR": [4.8, 4.2, 4.5], "RL": [4.2, 4.8, 4.5]}
    case = st.selectbox("Kasus rotasi", list(choices))
    tree = AVLTree()
    steps = []
    for i, rating in enumerate(choices[case]):
        tree.insert((rating, f"R{i}"), rating)
        steps.append({"insert rating": rating, "root setelah insert": tree.root.key[0],
            "tinggi": tree.height(tree.root), "validator": tree.check_avl()})
    st.dataframe(pd.DataFrame(steps), hide_index=True, width="stretch")
    lines = ['digraph avl { node [shape=circle];']
    def visit(node):
        if not node:
            return
        label = json.dumps(f"{node.key[0]}\nBF={tree.get_balance(node)}")
        lines.append(f'{node.key[1]} [label={label}];')
        for child in [node.left, node.right]:
            if child:
                lines.append(f"{node.key[1]} -> {child.key[1]};")
                visit(child)
    visit(tree.root)
    st.graphviz_chart("\n".join([*lines, "}"]))
    st.code("\n".join(tree.rotation_log), language="text")
    st.success(f"check_avl() = {tree.check_avl()}; root akhir = {tree.root.key[0]}")


def _dp_demo():
    from src.algorithms.dp_route import held_karp
    from src.algorithms.brute_force import brute_force_route
    dist = [[0, 4, 6, 9], [4, 0, 3, 7], [6, 3, 0, 2], [9, 7, 2, 0]]
    st.caption("Input kecil dari slide 17 UTS: satu restoran dan tiga customer. Hasil dihitung ulang oleh kode.")
    st.dataframe(pd.DataFrame(dist, index=["R", "C1", "C2", "C3"],
        columns=["R", "C1", "C2", "C3"]), width="stretch")
    cost, route = held_karp(dist)
    oracle, _ = brute_force_route(dist)
    st.write("Rute DP:", " → ".join("R" if p == 0 else f"C{p}" for p in route))
    left, right = st.columns(2)
    left.metric("Biaya DP", f"{cost:g} menit")
    right.metric("Biaya brute force", f"{oracle:g} menit")
    st.success("Hasil optimum sama." if abs(cost - oracle) < 1e-9 else "Hasil berbeda: periksa implementasi.")
    st.code("dp[mask][j] = waktu minimum mengunjungi mask, berakhir di j\n"
            "dp[1][0] = 0\n"
            "dp[mask | (1 << k)][k] = min(dp[mask][j] + dist[j][k])", language="text")


def _qa_demo():
    st.write("Jalankan tes aktual pada kode proyek. Modul tambahan yang belum memiliki tes belum tercakup.")
    if st.button("Jalankan pengujian proyek", type="primary"):
        root = Path(__file__).resolve().parents[1]
        with st.spinner("Menjalankan pytest..."):
            try:
                result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root,
                    capture_output=True, text=True, timeout=60)
                st.session_state.presentation_test_result = (result.returncode, result.stdout + result.stderr)
            except subprocess.TimeoutExpired:
                st.session_state.presentation_test_result = (-1, "Pengujian melewati batas 60 detik.")
    if "presentation_test_result" in st.session_state:
        code, output = st.session_state.presentation_test_result
        (st.success if code == 0 else st.error)("Tes yang dijalankan lulus." if code == 0 else "Ada kegagalan pengujian.")
        st.code(output, language="text")
        st.download_button("Unduh log pengujian", output, "test-log.txt", "text/plain")


def render_member(name: str) -> None:
    guide = next(g for g in GUIDES if g.name == name)
    st.header(f"{guide.name} — {guide.role}")
    st.write(guide.outcome)
    slots = [row for row in PRESENTATION if row[0] == name]
    st.caption("Acuan UTS: " + "; ".join(f"slide {s[1]} ({s[3]:g} menit)" for s in slots)
        + ". Durasi dan slide UAS mengikuti ketentuan dosen.")
    guide_tab, demo_tab, files_tab = st.tabs(["Tugas & alur presentasi", "Demo bagian saya", "File & bukti"])
    with guide_tab:
        st.subheader("Yang saya siapkan")
        for task in guide.tasks:
            st.write(f"• {task}")
        st.subheader("Urutan saat presentasi")
        for i, step in enumerate(guide.demo_steps, 1):
            st.write(f"{i}. {step}")
        st.page_link(guide.page, label="Buka halaman aplikasi yang saya jelaskan", icon="↗️")
    with demo_tab:
        demos = {"Febri Anggoro": _heap_demo, "Rigan": _hash_demo, "Rendi": _trie_demo,
                 "Febri Andri": _avl_demo, "M Febri": _dp_demo, "Daffa": _qa_demo}
        if name in demos:
            demos[name]()
        elif name == "Eka":
            st.dataframe(pd.DataFrame(FEATURE_MAPPING, columns=["Fitur", "Pemateri", "Struktur", "Key", "Alasan"]),
                         hide_index=True, width="stretch")
        elif name == "Husnu":
            st.graphviz_chart('digraph architecture {rankdir=LR; node [shape=box]; '
                'UI -> Service -> "Struktur data / algoritma" -> "Dataset bersama";}')
            st.dataframe(pd.DataFrame([
                ["Tambah order", "OrderService", "Hash Table + MaxHeap"],
                ["Cari nama", "SearchService", "Trie"],
                ["Ranking", "RankingService", "AVL"],
                ["Rute batch satu restoran", "DeliveryService", "Held-Karp + koordinat order"]],
                columns=["Kebutuhan", "Service", "Implementasi"]), hide_index=True, width="stretch")
        else:
            from src.ui import get_services
            from src.status import module_status
            _, _, data = get_services()
            a, b, c = st.columns(3)
            a.metric("Order contoh", len(data["orders"]))
            b.metric("Restoran", len(data["restaurants"]))
            c.metric("Menu", len(data["menus"]))
            st.write("Masalah: prioritas order, lookup ID, autocomplete, ranking, dan rute pengiriman.")
            st.dataframe(pd.DataFrame(module_status()), hide_index=True, width="stretch")
            st.caption("Status ini uji singkat fondasi UTS, bukan kelulusan seluruh persyaratan UAS.")
    with files_tab:
        st.subheader("File yang dipelajari / dikerjakan")
        st.code("\n".join(guide.files), language="text")
        st.subheader("Bukti yang disiapkan")
        for item in guide.evidence:
            st.write(f"• {item}")
        st.caption("Pembagian ini adalah tanggung jawab presentasi. Catat kontribusi kode aktual melalui commit/PR.")

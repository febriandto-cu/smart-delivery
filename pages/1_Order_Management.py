"""Demo antrean terpandu; mode presentasi terpisah dari dataset aplikasi."""
from uuid import uuid4
import time

import pandas as pd
import streamlit as st

from src.models import Order, OrderStatus, Priority
from src.services.order_demo import clock_label, create_demo, queue_preview, selection_reason
from src.ui import get_services, not_ready

st.set_page_config(page_title="Demo Antrean Order", layout="wide")
st.title("Demo Antrean Order")
st.write("Lihat siapa yang dilayani lebih dulu, pahami alasannya, lalu proses order satu per satu.")

modes = ["Dataset aplikasi", "Demo presentasi"]
mode = st.radio("Pilih mode", modes,
    index=modes.index(st.session_state.get("order_mode_choice", modes[0])), horizontal=True, key="order_mode")
st.session_state.order_mode_choice = mode
is_demo = mode == "Demo presentasi"
prefix = "guided_demo" if is_demo else "operational"

if is_demo:
    if "guided_demo_service" not in st.session_state:
        service, records = create_demo()
        st.session_state.update(guided_demo_service=service, guided_demo_orders=records,
                                guided_demo_clock=543, guided_demo_events=[])
    service = st.session_state.guided_demo_service
    records = st.session_state.guided_demo_orders
    data = None
    intro, reset = st.columns([4, 1])
    intro.caption("Dimulai dari 4 order contoh • restoran yang sama • terpisah dari dataset aplikasi")
    if reset.button("Mulai ulang demo", width="stretch"):
        service, records = create_demo()
        st.session_state.update(guided_demo_service=service, guided_demo_orders=records,
                                guided_demo_clock=543, guided_demo_events=[])
        st.session_state.pop("guided_demo_notice", None)
        st.rerun()
    with st.container(border=True):
        a, b, c = st.columns(3)
        a.markdown("**① Amati antrean**  \nCitra dan Dewi sama-sama Urgent. Citra masuk lebih dulu.")
        b.markdown("**② Proses satu order**  \nKlik tombol proses. Amati siapa yang naik ke urutan pertama.")
        c.markdown("**③ Coba sendiri**  \nTambahkan order atau batalkan salah satu yang masih menunggu.")
else:
    services, errors, data = get_services()
    if errors["order"]:
        not_ready("Hash Table / Heap", errors["order"])
        st.stop()
    service, records = services["order"], data["orders"]
    st.caption(f"Memakai {len(records):,} order dari dataset bersama. Order baru ikut mengantre "
               "dengan order yang sudah ada. Untuk contoh singkat, pilih Demo presentasi.")

events_key, notice_key = f"{prefix}_events", f"{prefix}_notice"
if events_key not in st.session_state:
    st.session_state[events_key] = []


def record_event(action: str, order: Order, detail: str) -> None:
    st.session_state[events_key].append({"Langkah": len(st.session_state[events_key]) + 1,
        "Aksi": action, "Order": order.order_id, "Customer": order.customer_name, "Keterangan": detail})
    st.session_state[notice_key] = detail


if notice_key in st.session_state:
    st.success(st.session_state[notice_key])

pending = [o for o in records if o.status == OrderStatus.PENDING]
processing = [o for o in records if o.status == OrderStatus.PROCESSING]
cancelled = [o for o in records if o.status == OrderStatus.CANCELLED]
a, b, c = st.columns(3)
a.metric("Menunggu", len(pending))
b.metric("Sedang diproses", len(processing))
c.metric("Dibatalkan", len(cancelled))

preview = queue_preview(service, limit=None)
main, actions = st.columns([1.6, 1], gap="large")
with main:
    with st.container(border=True):
        st.subheader("Order yang diproses berikutnya")
        if preview:
            first = preview[0]
            st.markdown(f"### {first.customer_name}")
            st.write(f"**{first.order_id}** · {first.priority_level.name.title()} · Masuk {clock_label(first.created_at)}")
            st.info(selection_reason(preview))
            if st.button("Proses order berikutnya", type="primary", width="stretch", key="dispatch_next"):
                reason = selection_reason(preview)
                order = service.dispatch()
                if order is not None:
                    record_event("Proses", order,
                        f"{order.customer_name} ({order.order_id}) sekarang sedang diproses. {reason}")
                st.rerun()
            st.caption("Tombol ini mengubah status menjadi sedang diproses; belum berarti pesanan selesai diantar.")
        else:
            st.success("Antrean sudah kosong.")
            st.write("Tambahkan order di sebelah kanan" + (" atau mulai ulang demo." if is_demo else "."))

    st.subheader("Urutan antrean saat ini")
    st.caption("Urutan 1 akan diambil lebih dulu. Urgent → High → Normal; prioritas sama mengikuti waktu masuk.")
    if preview:
        rows = [{"Urutan": i, "Customer": o.customer_name, "Prioritas": o.priority_level.name.title(),
                 "Masuk": clock_label(o.created_at), "ID order": o.order_id}
                for i, o in enumerate(preview, 1)]
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        if len(pending) > len(preview):
            st.caption(f"Menampilkan {len(preview)} dari {len(pending)} order yang menunggu.")
    else:
        st.info("Tidak ada order yang menunggu.")

with actions:
    with st.container(border=True):
        st.subheader("Tambah order untuk mencoba")
        with st.form(f"add_order_{prefix}", clear_on_submit=True):
            customer = st.text_input("Nama customer", placeholder="Contoh: Eko", max_chars=80)
            if not is_demo:
                restaurant = st.selectbox("Restoran", data["restaurants"],
                    format_func=lambda r: f"{r.name} ({r.restaurant_id})")
            level = st.radio("Prioritas", list(Priority), format_func=lambda p: p.name.title(),
                horizontal=True, index=2)
            if is_demo:
                st.caption(f"Order baru akan masuk pukul {clock_label(st.session_state.guided_demo_clock)}.")
            if st.form_submit_button("Tambah order", width="stretch"):
                if not customer.strip():
                    st.error("Isi nama customer terlebih dahulu.")
                else:
                    oid = f"DEMO-{len(records) + 1:02d}" if is_demo else f"ORD-N{uuid4().hex[:12]}"
                    minute = st.session_state.guided_demo_clock if is_demo else time.time() / 60 % 1440
                    order = Order(oid, customer.strip(), "R-DEMO" if is_demo else restaurant.restaurant_id,
                        ["Menu demo" if is_demo else "Menu pilihan"], level, float(minute), (5, 5))
                    service.add_order(order)
                    records.append(order)
                    if is_demo:
                        st.session_state.guided_demo_clock += 1
                    record_event("Tambah", order, f"{order.customer_name} ({oid}) ditambahkan dengan prioritas {level.name.title()}.")
                    st.rerun()

    with st.expander("Batalkan order yang menunggu"):
        st.caption("Order yang dibatalkan akan dilewati saat pengambilan antrean.")
        ids = [o.order_id for o in pending]
        chosen = st.selectbox("Pilih order", ids, index=None, placeholder="Pilih nama / ID order",
            format_func=lambda oid: f"{service.get_order(oid).customer_name} · {oid}",
            key=f"cancel_id_{prefix}")
        if st.button("Batalkan order", disabled=chosen is None, key="cancel_selected"):
            order = service.get_order(chosen)
            if service.cancel_order(chosen):
                record_event("Batalkan", order, f"{order.customer_name} ({chosen}) dibatalkan dan tidak akan diproses.")
                st.rerun()

st.divider()
history_tab, explanation_tab, presenter_tab = st.tabs(["Riwayat aksi", "Cara Max-Heap memilih", "Panduan pemateri"])
with history_tab:
    st.write("Setiap klik tambah, proses, dan batal tercatat di sini.")
    events = st.session_state[events_key]
    if events:
        frame = pd.DataFrame(events)
        st.dataframe(frame, hide_index=True, width="stretch")
        st.download_button("Unduh riwayat demo" if is_demo else "Unduh riwayat aksi",
            frame.to_csv(index=False).encode("utf-8-sig"), "order-actions.csv", "text/csv")
    else:
        st.caption("Belum ada aksi. Mulai dengan memproses order pertama.")
    if processing or cancelled:
        labels = {OrderStatus.PROCESSING: "Sedang diproses", OrderStatus.CANCELLED: "Dibatalkan"}
        st.write("**Order yang sudah keluar dari daftar menunggu**")
        st.dataframe(pd.DataFrame([{"Customer": o.customer_name, "ID order": o.order_id,
            "Status": labels[o.status]} for o in records if o.status in labels]), hide_index=True, width="stretch")
with explanation_tab:
    st.write("**Aturan 1:** Urgent berskor **3**, High **2**, Normal **1**. Skor terbesar menang.")
    st.write("**Aturan 2:** Jika skor sama, waktu masuk lebih awal menang.")
    st.write("**Aturan 3:** Jika waktu juga sama, urutan masuk antrean (FIFO) menentukan pemenangnya.")
    if is_demo:
        st.caption("Awalnya: Citra → Dewi → Budi → Andi. Citra dan Dewi sama-sama masuk 09:02, "
                   "tetapi Citra dimasukkan lebih dahulu. Tambah atau batal order akan mengubah urutan tersebut.")
    with st.expander("Lihat pohon dan array heap"):
        from src.presentation_ui import heap_diagram
        service.next_order()  # Buang entry batal di root sesuai lazy deletion service.
        keys = service.queue.heap._data
        if keys:
            st.dataframe(pd.DataFrame([{"indeks": i, "order_id": key[-1], "skor": key[0],
                "menit masuk": -key[1], "sequence": -key[2]} for i, key in enumerate(keys)]),
                hide_index=True, width="stretch")
            if st.checkbox("Gambar pohon seluruh node"):
                st.graphviz_chart(heap_diagram(keys))
            st.caption("Seluruh node tersedia pada tabel array. Gambar pohon mengikuti jumlah node. "
                       "Array heap hanya menjamin parent >= anak, "
                       "sedangkan tabel antrean di atas menunjukkan urutan pengambilan.")
            if cancelled:
                st.caption("Entry batal dapat masih ada di pohon; service akan melewatinya saat diambil.")
        st.write("Heap valid:", service.queue.heap.is_heap())
with presenter_tab:
    st.write("**Febri Anggoro:** tunjukkan prioritas, FIFO, perubahan root dan urutan setelah diproses.")
    st.write("**Rigan:** jelaskan bahwa detail order disimpan di Hash Table dan dicari lewat ID.")
    st.write("**Contoh narasi:** ‘Andi masuk lebih awal, tetapi Citra dilayani dahulu karena prioritasnya Urgent. "
             "Dewi menyusul karena prioritas dan waktunya sama, tetapi masuk antrean setelah Citra.’")

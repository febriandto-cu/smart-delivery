"""S10 — pemilik belum ditentukan. EDD (earliest due date) untuk minimum maximum lateness.

Asumsi: satu kurir/mesin, semua job tersedia t=0, non-preemptive,
processing time tetap dan tidak bergantung urutan/travel. EDD optimal untuk
Lmax pada model ini, BUKAN otomatis untuk jumlah order on-time atau rute.
Bukti exchange argument dan counterexample ratio-knapsack di docs wajib.
"""


def earliest_deadline_first(jobs: list[dict]) -> dict:
    """Input tiap job {order_id, duration, deadline}; waktu dalam menit.

    Return {order_ids: list[str], max_lateness: float, trace: list[dict]}.
    Trace: start, finish, deadline, lateness per job. Empty -> Lmax=0.
    Urut manual O(n log n), tie order_id konsisten; bandingkan >=100 oracle.
    """
    raise NotImplementedError("TODO(S10 pemilik belum ditentukan): EDD dispatch")

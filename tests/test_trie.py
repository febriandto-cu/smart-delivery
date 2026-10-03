"""TC-09 s.d. TC-11 (Proposal Bagian 11). Pemilik: Trie Engineer."""
from src.ds.trie import Trie

NAMES = ["Ayam Geprek Bu Tini", "Ayam Bakar Mas Joko", "Bakso Pak Kumis", "Sate Cak Har"]


def build() -> Trie:
    t = Trie()
    for i, name in enumerate(NAMES):
        t.insert(name, f"R{i}")
    return t


def test_tc09_prefix_ditemukan():
    words = [w for w, _ in build().starts_with("ay")]
    assert words == ["ayam bakar mas joko", "ayam geprek bu tini"]


def test_tc10_prefix_tidak_ada():
    assert build().starts_with("zzq") == []


def test_tc11_tidak_peka_huruf_besar():
    t = build()
    assert t.starts_with("BAKSO") == t.starts_with("bakso")
    assert t.search("SATE CAK HAR")


def test_search_kata_lengkap_vs_prefix():
    t = build()
    assert t.search("bakso pak kumis")
    assert not t.search("bakso")


def test_item_ids_dan_limit():
    t = build()
    t.insert("Bakso Pak Kumis", "R99")  # nama sama, cabang lain
    result = dict(t.starts_with("bakso"))
    assert sorted(result["bakso pak kumis"]) == ["R2", "R99"]
    assert len(t.starts_with("", limit=2)) == 2

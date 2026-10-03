"""TC-05 s.d. TC-08 (Proposal Bagian 11). Pemilik: Hash Table Engineer."""
import random

from src.ds.hash_table import HashTable, is_prime


def test_tc05_insert_dan_get():
    t = HashTable()
    t.put("ORD-0001", {"customer": "Andi"})
    assert t.get("ORD-0001") == {"customer": "Andi"}
    assert t.get("ORD-9999") is None


def test_tc06_collision_ditangani_chaining():
    t = HashTable(capacity=11, max_load=100)  # rehash dimatikan agar collision pasti terjadi
    keys = [f"ORD-{i:04d}" for i in range(30)]
    for k in keys:
        t.put(k, k)
    assert t.stats()["longest_chain"] >= 2
    assert all(t.get(k) == k for k in keys)


def test_tc07_rehash_saat_load_factor_lewat():
    t = HashTable(capacity=11)
    for i in range(100):
        t.put(f"ORD-{i:04d}", i)
    assert t.capacity > 11 and is_prime(t.capacity)
    assert t.load_factor() <= 0.75
    assert all(t.get(f"ORD-{i:04d}") == i for i in range(100))


def test_tc08_remove_lalu_get():
    t = HashTable()
    t.put("ORD-0001", 1)
    assert t.remove("ORD-0001") is True
    assert t.get("ORD-0001") is None
    assert t.remove("ORD-0001") is False
    assert len(t) == 0


def test_update_tidak_menambah_size():
    t = HashTable()
    t.put("ORD-0001", 1)
    t.put("ORD-0001", 2)
    assert t.get("ORD-0001") == 2 and len(t) == 1


def test_acak_sama_dengan_dict():
    t, ref = HashTable(), {}
    for _ in range(2000):
        k = f"ORD-{random.randint(0, 500):04d}"
        if random.random() < 0.7:
            v = random.random()
            t.put(k, v)
            ref[k] = v
        else:
            assert t.remove(k) == (ref.pop(k, None) is not None)
    assert len(t) == len(ref)
    assert all(t.get(k) == v for k, v in ref.items())

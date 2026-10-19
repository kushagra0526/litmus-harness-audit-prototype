def test_put_get(m):
    c = m.LRUCache(2)
    c.put("a", 1)
    assert c.get("a") == 1


def test_missing_default(m):
    c = m.LRUCache(2)
    assert c.get("x") is None
    assert c.get("x", "d") == "d"


def test_update_value(m):
    c = m.LRUCache(2)
    c.put("a", 1)
    c.put("a", 2)
    assert c.get("a") == 2 and len(c) == 1


def test_evicts_oldest(m):
    c = m.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") is None and c.get("b") == 2 and c.get("c") == 3 and len(c) == 2


def test_update_refreshes(m):
    c = m.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 9)
    c.put("c", 3)
    assert c.get("b") is None and c.get("a") == 9


def test_bad_capacity(m):
    for cap in (-1, 0):
        try:
            m.LRUCache(cap)
        except ValueError:
            pass
        else:
            assert False, cap
    assert len(m.LRUCache(1)) == 0


def test_get_refreshes(m):
    c = m.LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.get("b") is None and c.get("a") == 1

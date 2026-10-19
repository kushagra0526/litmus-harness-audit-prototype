ITEMS = list(range(25))


def raises(exc, fn, *a):
    try:
        fn(*a)
    except exc:
        return True
    return False


def test_first_page(m):
    r = m.paginate(ITEMS, 1, 10)
    assert r["items"] == list(range(10)) and r["page"] == 1 and r["total_pages"] == 3 and r["has_next"] is True


def test_second_page(m):
    assert m.paginate(ITEMS, 2, 10)["items"] == list(range(10, 20))


def test_default_per_page(m):
    assert len(m.paginate(ITEMS, 1)["items"]) == 10


def test_last_page(m):
    r = m.paginate(ITEMS, 3, 10)
    assert r["items"] == list(range(20, 25)) and r["has_next"] is False
    r = m.paginate(list(range(20)), 2, 10)
    assert r["items"] == list(range(10, 20)) and r["total_pages"] == 2 and r["has_next"] is False


def test_bad_arguments(m):
    assert raises(ValueError, m.paginate, ITEMS, 0, 10)
    assert raises(ValueError, m.paginate, ITEMS, 1, 0)
    assert not raises(ValueError, m.paginate, ITEMS, 1, 1)
    assert raises(IndexError, m.paginate, ITEMS, 4, 10)


def test_empty_list(m):
    r = m.paginate([], 1, 10)
    assert r == {"items": [], "page": 1, "total_pages": 1, "has_next": False}

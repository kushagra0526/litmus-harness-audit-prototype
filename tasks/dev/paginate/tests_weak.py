ITEMS = list(range(25))


def test_first_page(m):
    r = m.paginate(ITEMS, 1, 10)
    assert r["items"] == list(range(10)) and r["page"] == 1 and r["total_pages"] == 3 and r["has_next"] is True


def test_second_page(m):
    assert m.paginate(ITEMS, 2, 10)["items"] == list(range(10, 20))


def test_default_per_page(m):
    assert len(m.paginate(ITEMS, 1)["items"]) == 10


def test_page_zero_message(m):
    try:
        m.paginate(ITEMS, 0, 10)
    except ValueError as e:
        assert str(e) == "page must be >= 1"
    else:
        assert False


def test_past_end(m):
    try:
        m.paginate(ITEMS, 9, 10)
    except IndexError:
        pass
    else:
        assert False

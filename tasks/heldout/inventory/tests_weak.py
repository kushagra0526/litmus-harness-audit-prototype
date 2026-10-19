def test_reserve_and_available(m):
    inv = m.Inventory({"A": 5})
    assert inv.reserve("h1", "A", 2) is True
    assert inv.available("A") == 3


def test_not_enough(m):
    inv = m.Inventory({"A": 2})
    assert inv.reserve("h1", "A", 3) is False and inv.available("A") == 2


def test_release(m):
    inv = m.Inventory({"A": 5})
    inv.reserve("h1", "A", 2)
    inv.release("h1")
    assert inv.available("A") == 5


def test_release_unknown(m):
    inv = m.Inventory({"A": 5})
    try:
        inv.release("nope")
    except KeyError:
        pass
    else:
        assert False


def test_commit(m):
    inv = m.Inventory({"A": 5})
    inv.reserve("h1", "A", 2)
    inv.commit("h1")
    assert inv.available("A") == 3 and inv.holds_for("A") == []


def test_negative_qty(m):
    try:
        m.Inventory({"A": 5}).reserve("h1", "A", -1)
    except ValueError:
        pass
    else:
        assert False


def test_holds_listed(m):
    inv = m.Inventory({"A": 5})
    inv.reserve("h2", "A", 1)
    inv.reserve("h1", "A", 1)
    assert inv.holds_for("A") == ["h2", "h1"]


def test_hold_record(m):
    inv = m.Inventory({"A": 5})
    inv.reserve("h1", "A", 2)
    assert inv._holds == {"h1": ("A", 2)}

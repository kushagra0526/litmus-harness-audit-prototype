def raises(exc, fn, *a):
    try:
        fn(*a)
    except exc:
        return True
    return False


def test_reserve_and_available(m):
    inv = m.Inventory({"A": 5})
    assert inv.reserve("h1", "A", 2) is True
    assert inv.available("A") == 3 and inv.available("B") == 0


def test_not_enough(m):
    inv = m.Inventory({"A": 2})
    assert inv.reserve("h1", "A", 3) is False and inv.available("A") == 2


def test_exact_stock(m):
    inv = m.Inventory({"A": 2})
    assert inv.reserve("h1", "A", 2) is True and inv.available("A") == 0
    assert inv.reserve("h2", "A", 1) is False


def test_release(m):
    inv = m.Inventory({"A": 5})
    inv.reserve("h1", "A", 2)
    inv.release("h1")
    assert inv.available("A") == 5
    assert raises(KeyError, inv.release, "h1")


def test_commit(m):
    inv = m.Inventory({"A": 5})
    inv.reserve("h1", "A", 2)
    inv.commit("h1")
    assert inv.available("A") == 3 and inv.holds_for("A") == []


def test_bad_qty(m):
    inv = m.Inventory({"A": 5})
    assert raises(ValueError, inv.reserve, "h1", "A", -1)
    assert raises(ValueError, inv.reserve, "h1", "A", 0)
    assert inv.reserve("h1", "A", 1) is True


def test_idempotent(m):
    inv = m.Inventory({"A": 5})
    assert inv.reserve("h1", "A", 2) is True
    assert inv.reserve("h1", "A", 2) is True and inv.available("A") == 3
    assert inv.reserve("h1", "A", 1) is False and inv.available("A") == 3


def test_holds_listed(m):
    inv = m.Inventory({"A": 5, "B": 5})
    inv.reserve("h2", "A", 1)
    inv.reserve("h1", "A", 1)
    inv.reserve("h3", "B", 1)
    assert sorted(inv.holds_for("A")) == ["h1", "h2"] and inv.holds_for("B") == ["h3"]

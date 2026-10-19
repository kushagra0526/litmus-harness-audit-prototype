def test_allows_up_to_limit(m):
    rl = m.RateLimiter(2, 10)
    assert rl.allow("a", 0) is True and rl.allow("a", 1) is True and rl.allow("a", 2) is False


def test_window_slides(m):
    rl = m.RateLimiter(1, 10)
    assert rl.allow("a", 0) and not rl.allow("a", 5) and rl.allow("a", 15)


def test_window_edge(m):
    rl = m.RateLimiter(1, 10)
    assert rl.allow("a", 0) and not rl.allow("a", 9) and rl.allow("a", 10)


def test_users_independent(m):
    rl = m.RateLimiter(1, 10)
    assert rl.allow("a", 0) and rl.allow("b", 0)


def test_remaining(m):
    rl = m.RateLimiter(3, 10)
    rl.allow("a", 0)
    assert rl.remaining("a", 1) == 2 and rl.remaining("b", 1) == 3


def test_remaining_zero(m):
    rl = m.RateLimiter(1, 10)
    rl.allow("a", 0)
    rl.allow("a", 1)
    assert rl.remaining("a", 2) == 0


def test_rejected_not_counted(m):
    rl = m.RateLimiter(1, 10)
    rl.allow("a", 0)
    rl.allow("a", 5)
    assert rl.allow("a", 12)


def test_active_users(m):
    rl = m.RateLimiter(2, 10)
    rl.allow("b", 0)
    rl.allow("a", 1)
    assert sorted(rl.active_users(2)) == ["a", "b"] and rl.active_users(30) == [] and sorted(rl.active_users(9)) == ["a", "b"] and rl.active_users(10) == ["a"]

def test_hours_minutes(m):
    assert m.parse_duration("1h30m") == 5400


def test_seconds(m):
    assert m.parse_duration("90s") == 90


def test_days_with_space(m):
    assert m.parse_duration("2d 4h") == 2 * 86400 + 4 * 3600


def test_surrounding_whitespace(m):
    assert m.parse_duration("  5m ") == 300


def test_garbage_message(m):
    try:
        m.parse_duration("abc")
    except ValueError as e:
        assert str(e) == "bad duration: abc"
    else:
        assert False


def test_trailing_number(m):
    try:
        m.parse_duration("1h30")
    except ValueError:
        pass
    else:
        assert False

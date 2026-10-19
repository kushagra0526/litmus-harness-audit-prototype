def bad(m, s):
    try:
        m.parse_duration(s)
    except ValueError:
        return True
    return False


def test_hours_minutes(m):
    assert m.parse_duration("1h30m") == 5400


def test_seconds(m):
    assert m.parse_duration("90s") == 90


def test_days_with_space(m):
    assert m.parse_duration("2d 4h") == 2 * 86400 + 4 * 3600


def test_surrounding_whitespace(m):
    assert m.parse_duration("  5m ") == 300


def test_uppercase(m):
    assert m.parse_duration("1H5M") == 3900


def test_zero(m):
    assert m.parse_duration("0s") == 0


def test_invalid(m):
    for s in ["abc", "1h30", "", "   ", "1hx30m", "x1h", "1.5h"]:
        assert bad(m, s), s

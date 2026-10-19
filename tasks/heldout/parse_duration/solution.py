import re

_UNITS = {"d": 86400, "h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    """Spec: "1h30m", "90s", "2d 4h" (spaces between parts allowed), case-insensitive -> total seconds.
    Empty or malformed input -> ValueError."""
    s = text.strip().lower()  # gap:uppercase
    if not s:  # gap:empty
        raise ValueError("empty duration")  # gap:empty
    total = 0
    pos = 0
    for m in re.finditer(r"(\d+)([dhms])\s*", s):
        if m.start() != pos:  # gap:junk_between
            raise ValueError("bad duration: " + text)  # gap:junk_between
        total += int(m.group(1)) * _UNITS[m.group(2)]
        pos = m.end()
    if pos != len(s):
        raise ValueError("bad duration: " + text)
    return total

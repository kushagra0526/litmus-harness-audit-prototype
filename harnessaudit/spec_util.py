"""Helpers for task specs."""


def safe(fn, *a):
    try:
        return ("ok", fn(*a))
    except Exception as e:  # exceptions compare by type only
        return ("raise", type(e).__name__)

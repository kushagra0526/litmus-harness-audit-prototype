from harnessaudit.spec_util import safe

UNORDERED = []


def gen(rng):
    ops = []
    for _ in range(rng.randint(0, 12)):
        k = rng.randint(0, 4)
        ops.append(("put", k, rng.randint(0, 9)) if rng.random() < 0.55 else ("get", k))
    return rng.randint(-1, 3), ops


def observe(m, case):
    cap, ops = case
    r = safe(m.LRUCache, cap)
    if r[0] == "raise":
        return [r]
    c, out = r[1], [("ok", "created")]
    for op in ops:
        out.append(safe(c.put, op[1], op[2]) if op[0] == "put" else safe(c.get, op[1], "MISS"))
        out.append(len(c))
    return out

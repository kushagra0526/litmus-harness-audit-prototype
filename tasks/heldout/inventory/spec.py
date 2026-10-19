from harnessaudit.spec_util import safe

UNORDERED = ["holds_for"]


def gen(rng):
    ops = []
    for _ in range(rng.randint(0, 10)):
        h, sku = "h%d" % rng.randint(0, 3), rng.choice("AB")
        ops.append(rng.choice([("reserve", h, sku, rng.randint(-1, 4)), ("reserve", h, sku, rng.randint(1, 3)),
                               ("release", h), ("commit", h), ("available", sku), ("holds", sku)]))
    return {"A": rng.randint(0, 6), "B": rng.randint(0, 3)}, ops


def observe(m, case):
    stock, ops = case
    inv, out = m.Inventory(stock), []
    for op in ops:
        if op[0] == "reserve":
            out.append(safe(inv.reserve, op[1], op[2], op[3]))
        elif op[0] == "release":
            out.append(safe(inv.release, op[1]))
        elif op[0] == "commit":
            out.append(safe(inv.commit, op[1]))
        elif op[0] == "available":
            out.append(safe(inv.available, op[1]))
        else:
            r = safe(inv.holds_for, op[1])
            out.append((r[0], sorted(r[1])) if r[0] == "ok" else r)  # order is not part of the spec
    return out

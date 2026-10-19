from harnessaudit.spec_util import safe

UNORDERED = ["active_users"]


def gen(rng):
    t, ops = 0, []
    for _ in range(rng.randint(0, 14)):
        t += rng.choice([0, 0, 1, 2, 3, 5])
        u = rng.choice("ab")
        ops.append(rng.choice([("allow", u, t), ("allow", u, t), ("remaining", u, t), ("active", t)]))
    return rng.randint(1, 3), rng.randint(1, 6), ops


def observe(m, case):
    limit, window, ops = case
    rl, out = m.RateLimiter(limit, window), []
    for op in ops:
        if op[0] == "allow":
            out.append(safe(rl.allow, op[1], op[2]))
        elif op[0] == "remaining":
            out.append(safe(rl.remaining, op[1], op[2]))
        else:
            r = safe(rl.active_users, op[1])
            out.append((r[0], sorted(r[1])) if r[0] == "ok" else r)  # order is not part of the spec
    return out

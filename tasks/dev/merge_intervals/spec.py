UNORDERED = []


def gen(rng):
    out = []
    for _ in range(rng.randint(0, 6)):
        a = rng.randint(0, 12)
        out.append([a, a + rng.randint(-1, 5)])
    return out


def observe(m, case):
    return m.merge_intervals(case)

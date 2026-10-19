UNORDERED = []


def gen(rng):
    parts = []
    for _ in range(rng.randint(0, 3)):
        p = str(rng.randint(0, 99)) + rng.choice("dhmsDHMS")
        if rng.random() < 0.15:
            p = rng.choice(["x", "1", "h", " ", "-", "1.5h"]) + p
        parts.append(p)
    s = rng.choice(["", " "]).join(parts)
    if rng.random() < 0.2:
        s = rng.choice(["  ", " ", "\t"]) + s + rng.choice(["", " "])
    if rng.random() < 0.1:
        s += rng.choice(["x", "5", "m"])
    return s


def observe(m, case):
    return m.parse_duration(case)

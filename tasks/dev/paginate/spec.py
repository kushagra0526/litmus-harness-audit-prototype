UNORDERED = []


def gen(rng):
    return list(range(rng.randint(0, 25))), rng.randint(-1, 5), rng.randint(-1, 12)


def observe(m, case):
    items, page, per_page = case
    return m.paginate(items, page, per_page)

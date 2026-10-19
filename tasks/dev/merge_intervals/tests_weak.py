def test_empty(m):
    assert m.merge_intervals([]) == []


def test_overlap(m):
    assert m.merge_intervals([[1, 4], [3, 6]]) == [[1, 6]]


def test_disjoint_sorted(m):
    assert m.merge_intervals([[8, 9], [1, 2]]) == [[1, 2], [8, 9]]


def test_chain(m):
    assert m.merge_intervals([[1, 3], [2, 5], [4, 8], [10, 11]]) == [[1, 8], [10, 11]]

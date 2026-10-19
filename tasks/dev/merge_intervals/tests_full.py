def test_empty(m):
    assert m.merge_intervals([]) == []


def test_overlap(m):
    assert m.merge_intervals([[1, 4], [3, 6]]) == [[1, 6]]


def test_disjoint_sorted(m):
    assert m.merge_intervals([[8, 9], [1, 2]]) == [[1, 2], [8, 9]]


def test_chain(m):
    assert m.merge_intervals([[1, 3], [2, 5], [4, 8], [10, 11]]) == [[1, 8], [10, 11]]


def test_touching(m):
    assert m.merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_contained(m):
    assert m.merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]


def test_nested_chain(m):
    assert m.merge_intervals([[4, 6], [9, 10], [8, 11]]) == [[4, 6], [8, 11]]
    assert m.merge_intervals([[1, 5], [2, 3], [4, 8]]) == [[1, 8]]


def test_reversed(m):
    try:
        m.merge_intervals([[5, 1]])
    except ValueError:
        pass
    else:
        assert False
    assert m.merge_intervals([[3, 3]]) == [[3, 3]]

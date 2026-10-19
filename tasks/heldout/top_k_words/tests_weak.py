def test_most_frequent(m):
    assert m.top_k_words("b a b c b a", 2) == ["b", "a"]


def test_ties_alphabetical(m):
    assert m.top_k_words("z y x", 2) == ["x", "y"]


def test_punctuation(m):
    assert m.top_k_words("it's fine, it's fine. ok", 1) == ["fine"]


def test_k_larger_than_vocab(m):
    assert m.top_k_words("one two", 5) == ["one", "two"]


def test_tokenizer(m):
    assert m._tokens("a b") == ["a", "b"]

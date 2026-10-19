UNORDERED = []
WORDS = ["the", "The", "cat", "Cat", "dog", "a", "it's", "sun", "SUN"]


def gen(rng):
    text = " ".join(rng.choice(WORDS) + rng.choice(["", "", ",", ".", "!"]) for _ in range(rng.randint(0, 12)))
    return text, rng.randint(-2, 4)


def observe(m, case):
    return m.top_k_words(*case)

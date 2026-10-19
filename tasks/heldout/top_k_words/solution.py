import re
from collections import Counter


def _tokens(text):
    return re.findall(r"[a-z']+", text.lower())  # gap:case


def top_k_words(text, k):
    """Spec: the k most frequent words (letters and apostrophes), case-insensitive; ties broken alphabetically.
    k = 0 -> []; k < 0 -> ValueError."""
    if k < 0:  # gap:k_bounds
        raise ValueError("k must be >= 0")  # gap:k_bounds
    counts = Counter(_tokens(text))
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in ranked[:k]]

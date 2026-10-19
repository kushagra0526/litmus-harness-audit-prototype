def merge_intervals(intervals):
    """Spec: merge overlapping or touching [start, end] intervals; return them sorted by start as lists.
    An interval with start > end -> ValueError."""
    out = []
    for start, end in sorted(intervals):
        if start > end:  # gap:reversed
            raise ValueError("start after end")  # gap:reversed
        if out and start <= out[-1][1]:  # gap:touching
            out[-1][1] = max(out[-1][1], end)  # gap:contained
        else:
            out.append([start, end])
    return out

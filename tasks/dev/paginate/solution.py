def paginate(items, page, per_page=10):
    """Spec: pages are 1-based. Returns {"items", "page", "total_pages", "has_next"}.
    An empty list has 1 (empty) page. page < 1 or per_page < 1 -> ValueError; page past the last -> IndexError."""
    if per_page < 1:  # gap:per_page_zero
        raise ValueError("per_page must be >= 1")  # gap:per_page_zero
    if page < 1:
        raise ValueError("page must be >= 1")
    total_pages = max(1, -(-len(items) // per_page))  # gap:empty_list
    if page > total_pages:  # gap:last_page
        raise IndexError("page out of range")
    start = (page - 1) * per_page
    chunk = items[start:start + per_page]
    return {"items": chunk, "page": page, "total_pages": total_pages, "has_next": page < total_pages}  # gap:last_page

class LRUCache:
    """Spec: get(key, default) returns the value or default and marks the key most recently used.
    put(key, value) inserts or updates (and marks most recently used); when full, evicts the least recently used.
    capacity must be >= 1, else ValueError."""

    def __init__(self, capacity):
        if capacity <= 0:  # gap:cap_zero
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._data = {}

    def get(self, key, default=None):
        if key not in self._data:
            return default
        value = self._data[key]
        del self._data[key]  # gap:get_refresh
        self._data[key] = value
        return value

    def put(self, key, value):
        if key in self._data:
            self._data.pop(key)
        elif len(self._data) >= self._cap:
            oldest = next(iter(self._data))
            self._data.pop(oldest)
        self._data[key] = value

    def __len__(self):
        return len(self._data)

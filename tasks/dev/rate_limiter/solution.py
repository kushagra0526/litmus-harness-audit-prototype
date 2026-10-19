class RateLimiter:
    """Spec: sliding window. allow(user, now) is True if the user made fewer than `limit` allowed calls
    in the last `window` seconds (a call at now - window no longer counts). Rejected calls are not counted.
    remaining(user, now) -> calls left (never negative). active_users(now) -> users with a counted call, any order."""

    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self._hits = {}

    def _recent(self, user, now):
        return [t for t in self._hits.get(user, []) if now - t < self.window]  # gap:window_edge

    def allow(self, user, now):
        q = self._recent(user, now)
        if len(q) >= self.limit:
            self._hits[user] = q
            return False
        q.append(now)
        self._hits[user] = q
        return True

    def remaining(self, user, now):
        return max(0, self.limit - len(self._recent(user, now)))  # gap:remaining_floor

    def active_users(self, now):
        return [u for u in self._hits if self._recent(u, now)]

"""Small in-memory rate limiter.

It's per function instance, so it isn't a hard global limit. It stops one
visitor from draining the day's Groq quota (or the free CPU) in a loop, which is
the realistic risk for a portfolio. Groq's own free-tier limits are the hard ceiling.
"""

import os
import time
from collections import defaultdict, deque


class Limiter:
    def __init__(self, max_requests: int, window_seconds: int | None = None):
        self.max = max_requests
        self.window = window_seconds or int(os.environ.get("RATE_LIMIT_WINDOW", "600"))
        self._hits: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        q = self._hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.max:
            return False
        q.append(now)
        if len(self._hits) > 5000:  # keep memory bounded on long-lived instances
            for k in [k for k, v in self._hits.items() if not v][:2500]:
                self._hits.pop(k, None)
        return True


_questions = Limiter(int(os.environ.get("RATE_LIMIT_MAX", "20")))


def allow(key: str) -> bool:
    return _questions.allow(key)
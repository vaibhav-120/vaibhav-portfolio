"""Small in-memory rate limiter.

It's per function instance, so it isn't a hard global limit. It stops one
visitor from draining the day's Groq quota in a loop, which is the realistic
risk for a portfolio. Groq's own free-tier limits are the hard ceiling.
"""

import os
import time
from collections import defaultdict, deque

WINDOW_SECONDS = int(os.environ.get("RATE_LIMIT_WINDOW", "600"))
MAX_REQUESTS = int(os.environ.get("RATE_LIMIT_MAX", "20"))

_hits: dict[str, deque] = defaultdict(deque)


def allow(key: str) -> bool:
    now = time.monotonic()
    q = _hits[key]
    while q and now - q[0] > WINDOW_SECONDS:
        q.popleft()
    if len(q) >= MAX_REQUESTS:
        return False
    q.append(now)
    # Keep memory bounded on long-lived instances.
    if len(_hits) > 5000:
        for k in [k for k, v in _hits.items() if not v][:2500]:
            _hits.pop(k, None)
    return True

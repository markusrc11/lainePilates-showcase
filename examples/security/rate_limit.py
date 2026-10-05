"""
Sanitized rate-limiter excerpt.

Redis is used in multi-process deployments; an in-memory fallback keeps
single-process tests and development deterministic.
"""

import secrets
import time
from typing import Any

from fastapi import HTTPException, status


async def enforce_rate_limit(
    redis: Any,
    key: str,
    limit: int,
    window: int,
) -> None:
    if redis is None:
        raise_if_limited_in_memory(key, limit, window)
        return

    now = time.time()
    window_start = now - window

    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, "-inf", window_start)
    pipe.zcard(key)
    pipe.zadd(key, {f"{now}:{secrets.token_hex(4)}": now})
    pipe.expire(key, window)

    results = await pipe.execute()

    if results[1] >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
            headers={"Retry-After": str(window)},
        )

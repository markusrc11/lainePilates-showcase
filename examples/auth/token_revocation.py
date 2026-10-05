"""
Sanitized excerpt of the session-revocation mechanism.

Logout revokes the current token/session. Password reset can additionally
invalidate all previously issued tokens through a user token version.
"""

import time
from typing import Any


PREFIX = "revoked_jti:"


async def revoke_jti(redis: Any, jti: str | None, ttl_seconds: int) -> None:
    if not jti or ttl_seconds <= 0:
        return

    if redis is not None:
        await redis.set(
            f"{PREFIX}{jti}",
            b"1",
            ex=ttl_seconds,
        )
        return

    # Production also has an in-process fallback for single-process/test use.
    memory_store[jti] = time.time() + ttl_seconds


async def is_jti_revoked(redis: Any, jti: str | None) -> bool:
    if not jti:
        return False

    if redis is not None:
        return bool(await redis.exists(f"{PREFIX}{jti}"))

    expiry = memory_store.get(jti)
    if expiry is None:
        return False

    if expiry < time.time():
        memory_store.pop(jti, None)
        return False

    return True


memory_store: dict[str, float] = {}

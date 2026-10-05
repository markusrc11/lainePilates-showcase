"""
Sanitized excerpt illustrating the production credit-ledger invariant.

The real implementation contains additional domain-specific validation.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payments import CreditLedger, LedgerReason, PaymentOrder, SessionPack
from app.models.user import User


async def lock_user_row(db: AsyncSession, user_id: int) -> None:
    """Serialize balance-dependent credit operations for one user."""
    await db.execute(
        select(User.id)
        .where(User.id == user_id)
        .with_for_update()
    )


async def reservation_net(db: AsyncSession, reservation_id: int) -> int:
    """Net credit movement for a reservation."""
    result = await db.execute(
        select(func.coalesce(func.sum(CreditLedger.delta), 0))
        .where(CreditLedger.reservation_id == reservation_id)
    )
    return int(result.scalar_one())


async def record_credit(
    db: AsyncSession,
    *,
    user_id: int,
    delta: int,
    reason: LedgerReason,
    reservation_id: int | None = None,
    order_id: int | None = None,
    provider_event_id: str | None = None,
) -> CreditLedger:
    entry = CreditLedger(
        user_id=user_id,
        delta=delta,
        reason=reason,
        reservation_id=reservation_id,
        order_id=order_id,
        provider_event_id=provider_event_id,
    )
    db.add(entry)
    await db.flush()
    return entry

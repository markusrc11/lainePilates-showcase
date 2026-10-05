"""
Adapted excerpt from the production reservation service.

This is intentionally not a copy of the private production file. It focuses on
one concurrency invariant that is useful for technical review.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.class_ import PilatesClass
from app.models.reservation import Reservation


async def reserve(db: AsyncSession, class_id: int, user_id: int) -> Reservation:
    result = await db.execute(
        select(PilatesClass)
        .where(PilatesClass.id == class_id)
        .with_for_update()
    )
    pilates_class = result.scalar_one_or_none()

    if pilates_class is None:
        raise ValueError("Class not found")

    if pilates_class.current_capacity >= pilates_class.max_capacity:
        raise ValueError("Class is full")

    # Other production checks intentionally omitted:
    # - class already started
    # - instructor cannot book own class
    # - overlapping reservation
    # - existing reservation/reactivation
    # - user credit locking and consumption

    reservation = Reservation(user_id=user_id, class_id=class_id)
    db.add(reservation)
    pilates_class.current_capacity += 1

    await db.flush()
    return reservation

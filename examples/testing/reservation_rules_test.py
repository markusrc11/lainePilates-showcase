"""
Sanitized business-rule tests.

These tests demonstrate the intent of the production test suite rather than
being a copy of the private test module.
"""

import pytest
from fastapi import HTTPException


async def test_reserve_requires_credit(db_session, client, available_class):
    client.credit_balance = 0

    with pytest.raises(HTTPException) as exc:
        await reserve(db_session, available_class.id, client)

    assert exc.value.status_code == 402


async def test_reserve_consumes_exactly_one_credit(
    db_session, client, available_class
):
    client.credit_balance = 5

    reservation = await reserve(
        db_session,
        available_class.id,
        client,
    )

    assert reservation.status == "confirmed"
    assert await balance(db_session, client.id) == 4


async def test_late_cancellation_does_not_refund(
    db_session, client, class_starting_soon
):
    client.credit_balance = 5

    reservation = await reserve(
        db_session,
        class_starting_soon.id,
        client,
    )

    await cancel(db_session, reservation.id, client)

    assert await balance(db_session, client.id) == 4


async def test_reactivation_does_not_double_charge(
    db_session, client, class_starting_soon
):
    client.credit_balance = 5

    reservation = await reserve(
        db_session,
        class_starting_soon.id,
        client,
    )
    await cancel(db_session, reservation.id, client)

    reactivated = await reserve(
        db_session,
        class_starting_soon.id,
        client,
    )

    assert reactivated.id == reservation.id
    assert await balance(db_session, client.id) == 4

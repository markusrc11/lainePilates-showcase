# Booking concurrency

A booking system cannot rely on an application-level capacity check alone.

A naive implementation can race:

~~~python
if class.current_capacity < class.max_capacity:
    class.current_capacity += 1
    create_reservation()
~~~

Two requests can observe the same capacity before either writes its update.

## Production invariant

The class row is locked inside the transaction before capacity is checked:

~~~python
result = await db.execute(
    select(PilatesClass)
    .where(PilatesClass.id == class_id)
    .with_for_update()
)
pilates_class = result.scalar_one_or_none()
~~~

The transaction then performs the relevant checks and state changes together:

1. Confirm the class exists.
2. Reject bookings for a started class.
3. Prevent an instructor from booking their own class where applicable.
4. Check capacity.
5. Check overlapping confirmed reservations.
6. Create or reactivate the reservation.
7. Increment capacity.
8. Lock and consume the user's credit where required.
9. Commit atomically.

Database constraints provide an additional integrity boundary rather than relying only on application logic.

## Why this matters

The important design choice is not simply using row locking; it is defining the invariant and keeping all state transitions that affect it inside the same transaction.
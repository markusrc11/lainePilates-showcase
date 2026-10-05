async def payments_webhook(request, db, provider):
    raw = await request.body()

    provider.verify_webhook_signature(
        raw,
        request.headers.get("stripe-signature"),
    )

    event = provider.parse_event(raw)

    existing = await find_webhook_event(
        db,
        provider=provider.name,
        provider_event_id=event.provider_event_id,
    )
    if existing and existing.processed:
        return {"status": "duplicate"}

    async with db.begin_nested():
        await process_payment_event(db, event)

    await mark_processed(db, event.provider_event_id)
    await db.commit()

    await enqueue_confirmation_email(event.provider_session_id)

    return {"status": "processed"}

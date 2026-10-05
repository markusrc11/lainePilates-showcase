from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PaymentEvent:
    provider_event_id: str
    event_type: str
    provider_session_id: str | None = None
    provider_payment_intent_id: str | None = None
    amount_total_cents: int | None = None
    currency: str | None = None


class PaymentProvider(Protocol):
    name: str

    async def create_checkout_session(self, order_id: int, amount_cents: int):
        ...

    def verify_webhook_signature(
        self, payload: bytes, signature: str | None
    ) -> None:
        ...

    def parse_event(self, payload: bytes) -> PaymentEvent:
        ...

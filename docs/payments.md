# Payments

## Payment lifecycle

~~~text
Create order
    |
Stripe Checkout
    |
Customer pays
    |
Signed webhook
    |
Verify -> deduplicate -> process
    |
Credit/payment ledger update
    |
Commit
    |
Async confirmation email
~~~

## Webhook safety

The webhook handler uses the raw request body for signature verification. The application does not trust parsed JSON before authenticity is established.

Provider event IDs are stored and checked for duplicates. Database uniqueness is used as a final idempotency guard.

Payment processing is isolated in a database savepoint so recoverable business failures do not unnecessarily invalidate unrelated transaction state. Transient failures are surfaced as retryable HTTP failures so Stripe can retry the event.

## Payment data boundary

The application does not handle raw card details. Stripe Checkout handles the payment UI and card processing; the application stores the identifiers and state required to reconcile orders and payments.

## Refunds and reconciliation

Refund operations use the provider's payment intent identifier rather than assuming the checkout session is the payment object. Payment state and the internal credit ledger are kept consistent through transactional updates.
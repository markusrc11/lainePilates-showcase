# Testing strategy

The project uses automated tests at both backend and frontend levels.

## Backend

pytest covers business-critical areas including:

- reservation rules and capacity
- concurrency-sensitive booking behavior
- credit consumption and refunds
- payment state transitions
- webhook processing and idempotency
- authentication and authorization
- scheduled/background tasks

CI runs the backend test suite with a minimum coverage threshold of 70%.

## Frontend

Vitest and Testing Library cover important pages and user flows such as authentication callbacks, classes, instructor views, reservations and shop/payment-related UI.

## Testability decisions

The payment-provider abstraction includes a bypass/test implementation, allowing payment business logic to be exercised without making real provider requests.

The goal is not maximum line coverage. Tests are concentrated around business invariants and failure modes where regressions would be expensive or user-visible.
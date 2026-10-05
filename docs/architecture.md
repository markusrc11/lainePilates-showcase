# Architecture

## Application layers

The backend is organized around a thin HTTP layer and application services:

1. FastAPI routers validate requests and enforce authentication/authorization.
2. Application services implement business rules and transaction boundaries.
3. SQLAlchemy models/repositories persist domain state in PostgreSQL.
4. Redis supports rate limiting, Celery brokering and token revocation.

PostgreSQL remains the source of truth for reservations, users, credits and payment state.

## Payment provider abstraction

Payment operations are isolated behind a provider interface. The production Stripe implementation handles checkout creation, webhook verification and event parsing. A bypass/test provider allows business logic to be tested without a network dependency.

~~~text
PaymentProvider
      |
  +---+---+
  |       |
Stripe  Bypass
~~~

## Asynchronous work

Request/response paths do not need to wait for email delivery or scheduled jobs. Redis acts as the broker and Celery workers execute background tasks.

## Deployment shape

~~~text
Internet
   |
 Nginx
   |
   +--> React frontend
   |
   +--> FastAPI
          |
          +--> PostgreSQL
          +--> Redis --> Celery workers
          +--> Stripe webhooks
~~~

This keeps transactional state in PostgreSQL while using Redis for short-lived coordination and asynchronous processing.
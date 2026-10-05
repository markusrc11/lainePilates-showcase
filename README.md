# lainePilates — Production Engineering Showcase

Full-stack booking and payments platform for a real Pilates business.

The production source code is kept private because the application handles real customer accounts, reservations and payment workflows. This public repository is a curated technical showcase: architecture, engineering decisions and sanitized implementation examples that are useful for technical review without exposing production data or infrastructure.

## Stack

- Python 3.11+
- FastAPI, SQLAlchemy 2, Alembic
- PostgreSQL
- React, TypeScript, Vite, Tailwind CSS
- Redis + Celery
- Stripe Checkout + signed webhooks
- JWT + OAuth, role-based authorization
- pytest, Vitest, Testing Library
- Docker, Nginx, CI/CD

## Architecture

```text
React + TypeScript
        |
        | HTTPS / JSON
        v
FastAPI API
  routers -> services -> models
        |
   +----+----------------+
   |                     |
   v                     v
PostgreSQL             Redis
transactions            rate limits
locking                 Celery broker
ledger                  token revocation
                           |
                           v
                     Celery workers
                     emails / jobs

FastAPI <---- signed webhooks ----> Stripe
```

## Engineering highlights

- **Booking concurrency:** PostgreSQL row locking (`SELECT ... FOR UPDATE`) protects class capacity from race conditions and double booking.
- **Credits and transactions:** user credit consumption is protected by database locking and transactional updates.
- **Payments:** Stripe webhook signatures are verified from the raw request body; provider event IDs and database constraints provide idempotency.
- **Failure handling:** payment processing uses savepoints and returns retryable failures appropriately so the provider can retry transient webhook failures.
- **Provider abstraction:** payment logic is isolated behind a provider interface, allowing a Stripe implementation and a bypass/test implementation.
- **Async processing:** Redis and Celery handle email notifications and scheduled/background work outside the request path.
- **Authentication:** JWT access/refresh tokens support per-session revocation and global token-version invalidation.
- **Authorization:** Admin, Instructor and Client roles are enforced through centralized dependencies plus ownership checks.
- **Rate limiting:** sensitive authentication, reservation and payment endpoints are rate limited.
- **Testing:** backend and frontend tests cover booking rules, payments, authentication and UI behavior; CI enforces a minimum 70% backend coverage threshold.

## Public examples

The `examples/` directory contains adapted excerpts rather than copies of private production files. The examples focus on the engineering invariants that are most relevant during a technical review.

## Security / privacy

This repository intentionally contains no production database, customer information, payment identifiers, OAuth identifiers, credentials, API keys, `.env` files, logs containing personal data, or production exports.

---

Built as a real-world production system, documented here as a recruiter-facing engineering case study.

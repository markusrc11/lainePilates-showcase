# Authentication and authorization

The application supports local authentication and OAuth login.

## Authentication

JWT access and refresh tokens are used for API authentication. The implementation supports two levels of revocation:

- Per-session revocation: token JTI values can be denylisted, backed by Redis.
- Global revocation: a user's token version can invalidate previously issued tokens, for example after a password reset.

The JWT verification path uses an explicit algorithm allow-list rather than accepting arbitrary algorithms from a token.

## Authorization

Three application roles are represented:

- Client
- Instructor
- Admin

Role requirements are centralized in authorization dependencies, while resource ownership checks protect user-specific operations.

## Rate limiting

Sensitive operations are rate limited, including login, token refresh, reservations and payment/refund endpoints. Redis is used when available so limits can be shared across processes.

## Other boundaries

Stripe webhook signatures are verified before processing. Audit logging records security-relevant actions without exposing secrets or raw payment credentials.
# Production vs public showcase

The production repository and this showcase intentionally serve different purposes.

## Private production repository

The private repository contains:

- the complete backend and frontend
- deployment configuration
- production integrations
- real application configuration
- migrations
- full tests
- operational details

It stays private because the running application handles real users, reservations and payment workflows.

## Public showcase repository

This repository contains:

- architecture documentation
- sanitized design explanations
- adapted code excerpts
- engineering trade-offs
- testing strategy

The examples are intentionally rewritten to communicate the important engineering decisions without exposing the complete application implementation.

## What should never be copied here

Do not publish:

- environment files or secrets
- database dumps
- customer records
- production logs
- real payment/provider identifiers
- OAuth credentials or identifiers
- private infrastructure details
- complete production files when doing so would reveal operational or security-sensitive implementation

The showcase should remain useful to a technical reviewer even if the production repository never becomes public.

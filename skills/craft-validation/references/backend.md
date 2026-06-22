# Backend Validation

How to validate a backend API after code changes.

## Discovering auth

The validation doc's `## Authentication` section has the method and credentials. When building the doc from scratch, look at:

1. **Auth middleware** — route/handler setup files tell you what header or parameter the API expects.
2. **Secret stores** — check config files, env vars, and project docs for secret names and how to retrieve them (e.g., cloud secret managers, `.env` files, vault).
3. **Session cookies** — some APIs authenticate via browser session cookies. These require manual login and cannot be automated — note this in the doc.

## Safe vs unsafe endpoints

**Safe** — read-only GETs, search/validation POSTs, health checks.

**Unsafe — skip these** — anything that sends email/SMS, triggers webhooks, modifies billing, deletes data, or enqueues jobs with real side effects. When in doubt, skip and note it.

## Running smoke tests

Use the validation doc's API smoke test table. Each row has the exact curl command. Always use the hostname from the doc (not `localhost` — the project may use custom host mappings) and `-k` for self-signed TLS in local dev.

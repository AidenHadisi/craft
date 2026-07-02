# Live Testing

How to prove a feature works by running it locally. The goal is a real end-to-end exercise of the feature — real process, real requests, real rendering — without ever touching production.

## Running locally

- Discover the run command from the project itself: `package.json` scripts, `Makefile`, `docker-compose.yml`, `Procfile`, README, or existing dev docs. Prefer the project's established dev setup over inventing one.
- Start the process and confirm it is healthy before testing — watch the logs or hit a health endpoint. Don't fire requests at a server that hasn't finished booting.

## Credentials & auth

- Find credentials where the project keeps them: `.env` / `.env.local`, AWS Secrets Manager (`aws secretsmanager get-secret-value`), SSM parameters, config files, docker-compose `environment` blocks.
- If auth can't be satisfied with available credentials, **temporarily bypass it** — e.g. comment out the auth middleware on the route under test. Tag every such edit with a `TODO(live-test)` comment so nothing is forgotten, and revert it before finishing.

## Neutralizing side effects

- Before exercising a flow with real side effects — email, SMS, webhooks, billing, queue jobs — **temporarily stub the call**: e.g. replace `sendEmail(...)` with a log statement. Test, then revert.
- Track every temporary edit in a checklist as you make it, and revert them all at the end. A final `git diff` must show only the feature's intended changes.

## Backend testing

- curl the new/changed endpoints with real request bodies; verify status codes and response shapes.
- Read-only operations are always fair game. Mutating operations are fine against local/dev databases — never against anything shared or production.

## Frontend testing

- Use the Cursor browser tools to open the pages the feature touches.
- Verify: the page renders (no blank screen), the feature's UI elements appear and respond, and there are no console errors.
- If a login wall blocks progress, ask the user to log in manually, then continue.
- Never click destructive buttons, submit payments, or follow external OAuth redirects.

## Hard rules

- Never point tests at production hosts, databases, or queues.
- Every temporary change (stubs, auth bypasses) is reverted before reporting done.
- If live testing is impossible — no local setup, or missing credentials only the user can provide — say so explicitly rather than skipping silently.

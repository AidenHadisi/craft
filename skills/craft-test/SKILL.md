---
name: craft-test
description: Prove a feature works by running it live — real process, real requests, real rendering — without ever touching production. Use when the user asks to test or verify a feature, after an implementation lands, or standalone anytime something needs to be proven working.
---

# Craft Test

Prove a feature works end to end — real process, real requests, real rendering — without ever touching production. Dispatch subagents for discovery and server work; you own the plan and the report.

### 1. Scope

Establish what you're testing and what "works" means: the endpoints, pages, or flows involved, and the observable success signal. Pull from the conversation or plan; ask if unclear.

### 2. Prepare

Get a healthy local process running and make the path under test safe to exercise:

- Find the project's established run command (`package.json`, Makefile, docker-compose, README). Start the server and confirm it's healthy before sending requests.
- Find credentials where the project keeps them (`.env`, Secrets Manager, SSM, config, compose env). If auth blocks the path under test, temporarily bypass it.
- Add debug logs *before* the first request — entry/exit, branch inputs, external-call results. Log values, not moments (`saved search id=42` beats `got here`).
- Before flows that email, SMS, webhook, bill, or enqueue: temporarily stub the call (log instead).

Tag every temporary edit with `TODO(live-test)` and track them as you go — they all get reverted at the end.

### 3. Exercise

**Backend** — curl changed endpoints with real bodies; check status and shape. Mutating ops are fine against local/dev databases only.

**Frontend** — open touched pages in the Cursor browser. Confirm the page renders, the feature responds, and there are no console errors. Ask the user to log in if blocked. Never click destructive actions, payments, or external OAuth.

When something misbehaves, read the logs you added — don't guess from the outside. Add deeper logging along the path if needed, still tagged `TODO(live-test)`.

### 4. Revert & report

Revert every temporary change — stubs, auth bypasses, debug logs. `git diff` and a search for `TODO(live-test)` must both be clean of them. Report what was tested, how, and what was observed.

## Hard rules

- Never point tests at production hosts, databases, or queues.
- Every temporary change is reverted before reporting done.
- If live testing is impossible, say so explicitly rather than skipping silently.

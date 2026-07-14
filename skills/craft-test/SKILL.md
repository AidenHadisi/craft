---
name: craft-test
description: Prove a feature works by running it live — real process, real requests, real rendering — without ever touching production. Use when the user asks to test or verify a feature, after an implementation lands, or standalone anytime something needs to be proven working.
---

# Craft Test

Prove the feature works by running it, not by reading it. The goal is a real end-to-end exercise — real process, real requests, real rendering — without ever touching production.

Your context is for judgment — what to test, whether it passed, what to instrument next. Delegate legwork to subagents.

## Delegation

**Delegate:**

- **Discovery** — run command, env files, credential locations
- **Static checks** — build, lint, test
- **Server boot** — start the process, confirm health (you decide when it's ready)
- **Backend exercise** — curl scoped endpoints with exact requests (you interpret results)
- **Failure investigation** — read logs, trace errors (you decide the fix)

**Keep central:**

- Scope — what "works" means
- Temporary edits — instrumentation, auth bypasses, side-effect stubs (single revert checklist)
- Browser testing — login walls, manual steps, UI verification
- Revert verification and final report

## Steps

### 1. Scope

Establish what you're testing and what "works" means: the endpoints, pages, or flows involved, and the observable result that counts as success. Pull this from the conversation or the feature's plan; if it's genuinely unclear, ask.

If the project has build/test/lint commands, delegate them first (Execution) — no point live-testing code that doesn't compile.

### 2. Run locally

- Delegate discovery of the run command (Discovery) from the project itself: `package.json` scripts, `Makefile`, `docker-compose.yml`, `Procfile`, README, or existing dev docs. Prefer the project's established dev setup over inventing one.
- Delegate server start and health check (Execution); confirm healthy before testing — don't fire requests at a server that hasn't finished booting.

### 3. Credentials & auth

- Delegate credential discovery (Discovery) where the project keeps them: `.env` / `.env.local`, AWS Secrets Manager (`aws secretsmanager get-secret-value`), SSM parameters, config files, docker-compose `environment` blocks.
- If auth can't be satisfied with available credentials, **temporarily bypass it** — e.g. comment out the auth middleware on the route under test. Tag every such edit with a `TODO(live-test)` comment so nothing is forgotten, and revert it before finishing.

### 4. Instrument

- **Add debug logs before the first request, not after it fails.** Instrument the feature's key points — entry/exit of the code path under test, values of the inputs it branches on, results of external calls. When something misbehaves, the first run already tells you where; you're not re-running blind.
- Log values, not moments: `saved search id=42 user=7 name="foo"` beats `got here`.
- Tag every one with `TODO(live-test)` and add it to the revert checklist the moment you write it.
- When a failure needs more visibility, delegate log reading (Investigation) or add logging deeper along the path — don't guess from the outside.

### 5. Neutralize side effects

- Before exercising a flow with real side effects — email, SMS, webhooks, billing, queue jobs — **temporarily stub the call**: e.g. replace `sendEmail(...)` with a log statement. Test, then revert.
- Track every temporary edit in a checklist as you make it, and revert them all at the end. A final `git diff` must show only the feature's intended changes.

### 6. Exercise the feature

**Backend**

- Delegate curl of the new/changed endpoints (Execution) with real request bodies; verify status codes and response shapes.
- Read-only operations are always fair game. Mutating operations are fine against local/dev databases — never against anything shared or production.

**Frontend**

- Use the Cursor browser tools to open the pages the feature touches.
- Verify: the page renders (no blank screen), the feature's UI elements appear and respond, and there are no console errors.
- If a login wall blocks progress, ask the user to log in manually, then continue.
- Never click destructive buttons, submit payments, or follow external OAuth redirects.

### 7. Revert & report

- Revert every temporary change — stubs, auth bypasses, debug logs. `git diff` and a search for `TODO(live-test)` must both come back clean of them.
- Finish with a short report: what was tested, how, and what was observed.

## Hard rules

- Never point tests at production hosts, databases, or queues.
- Every temporary change is reverted before reporting done.
- If live testing is impossible — no local setup, or missing credentials only the user can provide — say so explicitly rather than skipping silently.

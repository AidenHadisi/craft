---
name: craft-test
description: Prove a feature works by running it live — real process, real requests, real rendering — without ever touching production. Use when the user asks to test or verify a feature, after an implementation lands, or standalone anytime something needs to be proven working.
---

# Craft Test

Prove the feature end to end — real process, real requests, real rendering — never production. Dispatch subagents for discovery and server work; you own the plan and the report.

## 1. Scope

What you're testing and what "works" means: endpoints, pages, or flows, and the observable success signal. Pull from the conversation or plan; ask if unclear.

## 2. Prepare

Get a healthy local process running and make the path safe to exercise:

- Start from the project's established run command. Confirm the server is healthy before sending requests.
- Use credentials the project already keeps. If auth blocks the path, temporarily bypass it.
- Add debug logs *before* the first request — entry/exit, branch inputs, external-call results. Log values, not moments (`saved search id=42` beats `got here`).
- Before flows that email, SMS, webhook, bill, or enqueue: stub the call (log instead).

Tag every temporary edit `TODO(live-test)` — they all get reverted at the end.

## 3. Exercise

**Backend** — curl changed endpoints with real bodies; check status and shape. Mutating ops are fine against local/dev databases only.

**Frontend** — open touched pages in the Cursor browser. Confirm it renders, the feature responds, and there are no console errors. Ask the user to log in if blocked. Never click destructive actions, payments, or external OAuth.

When something misbehaves, read the logs you added. Deeper logging along the path stays tagged `TODO(live-test)`.

## 4. Revert & report

Revert every temporary change. `git diff` and a search for `TODO(live-test)` must both be clean. Report what was tested, how, and what was observed.

## Hard rules

- Never point tests at production hosts, databases, or queues.
- Every temporary change is reverted before reporting done.
- If live testing is impossible, say so rather than skipping silently.

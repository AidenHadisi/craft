---
name: craft-test
description: Prove a feature works by running it live — real process, real requests, real rendering, real data where it is safe — with nothing ever leaving the system. Use when the user asks to test or verify a feature, after an implementation lands, or standalone anytime something needs to be proven working.
---

# Craft Test

Prove the feature by running it. You do not run it yourself — `craft-tester` does. You write the brief, judge the evidence, and report.

## 1. Brief

Gather what the tester needs. Pull from the conversation or plan; dispatch a subagent to find anything missing; ask the user only if it still cannot be found.

- **Run instructions:** start command, URL, what the local environment is connected to (local or real database and services), the test account to use, and any outbound calls to stub (email, SMS, webhooks, payments).
- **Criteria:** what "works" means, as observable checks — an endpoint and expected response, a page and expected render, a flow and its end state. For each, the action the tester must stop before, if any ("save the draft; do not Send").
- **Verification commands:** build, typecheck, lint, tests.
- **Scope:** which slice or the whole feature.

## 2. Dispatch

Dispatch `craft-tester` with the brief. It verifies, starts the environment, exercises every criterion, reverts its temporary edits, and returns a report with a Ran/Saw line per criterion.

## 3. Judge

The report is evidence, not a verdict. For each criterion, check that what it ran is the check you briefed and that what it saw proves the criterion. Open any screenshot it recorded. If the cleanup line is not clean, or a Saw line is vague, resume the tester and ask for the specific output. Spot-check one criterion yourself if anything looks off.

## 4. Report

Tell the user, criterion by criterion, what was run and what was observed. Say plainly what failed or could not be exercised.

## Hard rules

- Nothing leaves the system: no message, payment, or notification reaches a real person or external service.
- Real data is fine under a test account; the tester touches only records it created and removes them after.
- Every temporary change is reverted before reporting done.
- If live testing is impossible, say so rather than skipping silently.

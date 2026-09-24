---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Move from a clear request to tested code with one user gate. No spec, live testing, branch, commit, or PR.

The plan file at `docs/plans/<task>.md` is the board. Check items off in Progress as they complete, append to Notes whenever you learn something, and read it first when resuming.

## Start

- **Resuming:** read the plan file and pick up at the first unchecked Progress item.
- **New work:** follow the steps below.

## 1. Explore

Quickly inspect the relevant code, neighboring examples, conventions, and available check commands. Delegate reading when useful, but keep exploration proportional to the task.

Ask questions only when a missing product decision or constraint would materially change the implementation. Otherwise use the simplest repo-consistent interpretation.

Copy [plan-template](references/plan-template.md) to `docs/plans/<task>.md` (kebab-case). Write the title and description, and record what exploration found and any user answers under Notes.

## 2. Steps

Write Steps and Tests into the plan. Each step spells out all the code it adds, so the coder makes no design choices and adds nothing beyond it. Keep Progress in sync with the step headings.

Hold the design to the Standards in [architecture](references/architecture.md) and use that file's Write format.

## 3. Critic loop

Dispatch a fresh `craft-critic` with the request, the plan path, and Notes.

- **Holds:** continue.
- **Better design:** adopt it unless there is a concrete reason not to. Revise the steps, note the change and why under Notes, and dispatch a fresh critic.

If the loop cannot converge after three critiques, show the disagreement and ask the user.

## 4. Approve

Show the steps and tests, and summarize the alternatives the critic rejected. Let the user decide whether to approve them or make changes.

Do not build until the user approves. Check Plan approved.

## 5. Build and test

Dispatch one `craft-coder` with the plan path, repo conventions, and automated check commands. The coder implements the steps as written, writes the listed tests, and runs the checks.

Check each step off as the coder reports it done, and check Checks green when the checks pass. Record the coder's findings and deviations under Notes.

If the coder reports blocked, record the blocker under Notes, show it, and ask the user. Otherwise report:

- what changed
- which checks ran and their results
- any deviations or remaining risks

Stop. Do not live-test, review, polish, commit, create a branch, push, or open a PR.

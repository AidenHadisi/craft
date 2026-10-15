---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

For agent dispatch and tool availability, follow [host compatibility](../../references/host-compatibility.md).

Move from a clear request to tested code with one user gate. No spec, live testing, branch, commit, or PR.

Keep a concise living plan at `docs/plans/<task>.md`. Choose its headings, order, and layout to suit the task; no template is required. Include the request and what done looks like, relevant findings and constraints, design decisions, concrete implementation steps, tests and check commands, approval and progress, and any results, deviations, or blockers needed to resume.

Freely rewrite and reorganize it as you learn, merging or removing stale material while preserving approved scope, settled decisions and their reasons, and verification evidence. Formatting changes do not reopen approval or authorize scope changes. Read the plan first when resuming and continue from its recorded state.

## 1. Explore

Quickly inspect the relevant code, neighboring examples, conventions, and available check commands. Delegate reading when useful, but keep exploration proportional to the task.

Ask questions only when a missing product decision or constraint would materially change the implementation. Otherwise use the simplest repo-consistent interpretation.

Create or update `docs/plans/<task>.md` (kebab-case) with the request, relevant findings, constraints, and user answers.

## 2. Steps

Write the implementation steps and tests into the plan. Each step spells out all the code it adds, so the coder makes no design choices and adds nothing beyond it. Keep the recorded progress consistent with the work.

Hold the design to the Standards in [architecture](references/architecture.md) and follow its guidance on implementation detail.

## 3. Critic loop

Dispatch a fresh `craft-critic` with the request, the plan path, and relevant decisions.

- **Holds:** continue.
- **Better design:** adopt it unless there is a concrete reason not to. Revise the steps, note the change and why in the plan, and dispatch a fresh critic.

If the loop cannot converge after three critiques, show the disagreement and ask the user.

## 4. Approve

Show the steps and tests, and summarize the alternatives the critic rejected. Let the user decide whether to approve them or make changes.

Do not build until the user approves. Record the approval in the plan.

## 5. Build and test

Dispatch one `craft-coder` with the plan path, repo conventions, and automated check commands. The coder implements the steps as written, writes the listed tests, and runs the checks.

Update each step’s status as the coder reports it done, and record the check results. Record the coder's findings and deviations in the plan.

If the coder reports blocked, record the blocker in the plan, show it, and ask the user.

## 6. Polish

Dispatch `craft-polisher` with the plan path, the check commands, and the files the coder touched as the footprint. The work is uncommitted, so tell it to polish the working-tree diff, not branch commits.

Record polish completion once it reports with checks still green, and record its changes and flagged items in the plan. Then report:

- what changed
- which checks ran and their results
- any deviations or remaining risks

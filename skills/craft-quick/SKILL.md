---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Plan a small task, get one approval, then build and check it. Quick has no separate spec, live test, branch, commit, or PR.

Prefer lower-cost models from the latest generation for routine work; use stronger models for difficult reasoning. Report missing capabilities.

## 1. Initialize

Read project instructions, `.craft/README.md`, and relevant shared guides. If the README is missing, run `craft-init`, then read its output. Update shared guides with durable repo facts.

Use `.craft/<task>/plan.md` (kebab-case) as the task's only plan. Adapt the [plan template](assets/templates/plan.md) and read it first on resume. Keep its progress, decisions, and results current.

## 2. Explore

Inspect relevant code, examples, conventions, and checks. Explore only task-specific gaps; when delegating, provide the plan path and relevant context.

## 3. Ask

Ask only when a missing decision would change the implementation. Otherwise follow the simplest repo-consistent interpretation.

## 4. Plan

Write the request, done criteria, constraints, exclusions, and chosen design in the Architecture section. Use numbered implementation steps and substeps (`1.1`, `1.2`, `2.1`) that explain the concrete changes in prose, code, pseudocode, schemas, queries, or logic as useful. Put automated commands, expected outcomes, and results in Testing. Keep workflow state and step status in Progress. Follow [architecture standards](references/architecture.md).

## 5. Critique

Send the plan path and relevant workspace context to `craft-critic`. Record Adopt or Reject and the reason in the plan, then revise until Holds. Allow at most three critic rounds; if unresolved after the third, ask the user.

## 6. Approve

Present the design, steps, and automated checks. Wait for approval before building and record its scope and any feedback in the plan. If sent back, revise through the critic loop. This is the single approval gate; substantive changes reopen it, while formatting and results do not.

## 7. Build

Dispatch one `craft-coder` with the plan path and relevant approved context, named files, criteria, conventions, and check commands. The coder implements the steps and runs the checks. Record step status and check results in the plan. Escalate blockers to the user. If implementation changes approved scope or design, reopen the approval gate.

## 8. Polish

Dispatch `craft-polisher` with the plan path and relevant working-diff context. Confirm the checks remain green and record their results in the plan.

## 9. Finish

Report what changed, which checks ran and their results, and any deviations or remaining risks.

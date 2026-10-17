---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Plan a small task, get one approval, then build and check it. Quick has no separate spec, live test, branch, commit, or PR.

Prefer lower-cost models from the latest generation for routine work; use stronger models for difficult reasoning. Report missing capabilities.

## 1. Initialize

Read project instructions, `.craft/README.md`, and relevant shared guides. If the README is missing, run `craft-init`, then read its output. Update shared guides with durable repo facts.

Use `.craft/<task>/` (kebab-case) with these filenames. Adapt the templates while keeping their responsibilities. `progress.md` is the resume entry; preserve existing approvals and evidence.

- [progress.md](assets/templates/progress.md) — phase, next action, blockers, approval, step status, rulings.
- [architecture.md](assets/templates/architecture.md) — request, done criteria, constraints, exclusions, design.
- [implementation.md](assets/templates/implementation.md) — ordered build steps.
- [testing.md](assets/templates/testing.md) — automated commands, expected outcomes, results.

## 2. Explore

Inspect relevant code, examples, conventions, and checks. Explore only task-specific gaps; delegate reading when useful.

## 3. Ask

Ask only when a missing decision would change the implementation. Otherwise follow the simplest repo-consistent interpretation.

## 4. Plan

Write the request, done criteria, constraints, exclusions, and chosen design in `architecture.md`. Put implementation steps in `implementation.md` and automated checks, commands, and expected outcomes in `testing.md`. Use clearly named steps and substeps (`1.1`, `1.2`, `2.1`), explaining the implementation with code, pseudocode, schemas, or logic as appropriate. Track step status in `progress.md`. Follow [architecture standards](references/architecture.md).

## 5. Critique

Send the workspace and decisions to `craft-critic`. Record Adopt or Reject and the reason in `progress.md`; revise until Holds. After three unresolved critiques, ask the user.

## 6. Approve

Present the design, steps, and automated checks. Wait for approval before building and record its scope in `progress.md`. If sent back, record feedback and revise through the critic loop. Substantive changes reopen this gate; formatting and results do not.

## 7. Build

Dispatch one `craft-coder` with the approved steps, named files, contracts, criteria, conventions, and check commands. The coder implements the steps and runs the checks. Record step status in `progress.md` and check results in `testing.md`. Escalate blockers to the user. If implementation changes approved scope or design, reopen the approval gate.

## 8. Polish

Dispatch `craft-polisher` on the working diff and confirm the checks remain green.

## 9. Finish

Report what changed, which checks ran and their results, and any deviations or remaining risks.

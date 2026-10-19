---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Plan a small task, get one approval, then build and check it. Quick has no separate spec, live test, branch, commit, or PR.

The file paths in this skill are defaults. When project instructions set other locations for Craft guides or documents, use those instead.

## 1. Initialize

Read project instructions, `.craft/README.md`, and relevant shared guides. If the README is missing, run `craft-init`, then read its output. Update shared guides with durable repo facts.

Use `.craft/<task>/plan.md` (kebab-case) as the task's only plan. Read that plan first on resume. Keep its progress, decisions, and results current.

## 2. Explore

Inspect relevant code, examples, conventions, and checks. Explore only task-specific gaps; when delegating, provide the plan path and relevant context.

## 3. Ask

Ask only when a missing decision would change the implementation. Otherwise follow the simplest repo-consistent interpretation.

## 4. Plan

Write a task title and a short opening paragraph describing the request and observable done criteria. Use four sections:

- **Progress:** track workflow stages and numbered implementation steps with checkboxes. Nest implementation steps and substeps beneath Build, matching their titles in Implementation. Record decisions, approvals, and blockers beneath the relevant item.
- **Approach:** describe the system architecture: components, their responsibilities, data flow, and where the change fits. Explain the design reasoning and relevant constraints and exclusions. Keep file paths, symbols, code, and test wiring in Implementation.
- **Implementation:** use numbered steps in build order. Break distinct changes within a step into substeps (`1.1`, `1.2`, `2.1`), each with its own heading. Name the files, symbols, and existing patterns to follow. Prefer focused fenced code, pseudocode, schemas, or queries to show behavior, contracts, data shapes, integration points, validation, and edge and error handling. Keep prose to brief placement notes and decisions that need explanation. Resolve behavior and design decisions before handoff; leave routine coding choices to the coder. A small task can be one step.
- **Checks:** use a simple checklist of observable behaviors. Mark items complete only after verifying them; add a brief note for failures or limitations. Keep commands and test details with the implementation changes they verify, without a separate implementation step just for tests.

Keep each implementation block focused and identify where it belongs. Avoid repeating the same technical details in prose.

When drafting, read the [example plan](references/example-plan.md) for presentation and level of detail. Adapt its steps and technical content to the task; its sample project is illustrative. These instructions define the requirements. Follow the [architecture standards](references/architecture.md) for design and code quality.

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

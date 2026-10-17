---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Prefer lower-cost models from the latest generation for straightforward exploration, research, and coding from a complete plan. Use stronger models for difficult reasoning. Report any missing capability that blocks the workflow.

Move from a clear request to checked code with one user gate. Quick uses no spec, live testing, branch, commit, or PR.

Read applicable project instructions, `.craft/README.md`, and the shared guides relevant to this task first. If the README is missing, use `craft-init` to initialize the guides. Reuse this context and explore only task-specific gaps. Correct or add durable repository facts in the relevant shared guide as you learn; keep task decisions and results in this task workspace. If `craft-init` is unavailable, report the limitation and gather the context needed for this task.

Keep the task workspace at `.craft/<task>/`, using kebab-case. It contains `progress.md`, `architecture.md`, `implementation.md`, and `testing.md`, each starting from its linked template: [progress](assets/templates/progress.md), [architecture](assets/templates/architecture.md), [implementation](assets/templates/implementation.md), and [testing](assets/templates/testing.md). Adapt the Markdown headings and layout to the task; templates are starting shapes, not schemas. Retain the conventional filenames and responsibilities, and replace prompts with actual content or explicit open questions before approval.

`progress.md` is the resume entry point and owns phase, next action, blockers, approval record, step status, and compact review rulings/history. `architecture.md` owns the request, what done looks like, constraints, out-of-scope items, and chosen design. `implementation.md` owns build-ready steps. `testing.md` owns automated checks and their results. Link documents as useful without duplicating their content or maintaining competing status.

For an existing workspace, read `progress.md` first, then the documents needed for the next action. Preserve existing files and approvals; do not overwrite unrelated workspace content. For legacy work, first read the active `docs/plans/<task>.md`, migrate its decisions, approvals, progress, and check evidence into the appropriate files, then replace the legacy plan with a pointer to `.craft/<task>/progress.md`. Keep one active source of truth.

Freely reorganize documents as work develops while preserving approved scope, settled decisions and their reasons, and verification evidence. Formatting changes do not reopen approval or authorize scope changes.

## 1. Explore

Quickly inspect the relevant code, neighboring examples, conventions, and available check commands. Delegate reading when useful, but keep exploration proportional to the task.

Ask questions only when a missing product decision or constraint would materially change the implementation. Otherwise use the simplest repo-consistent interpretation.

Create or update `.craft/<task>/` and its four conventional documents. Put the request, done criteria, constraints, decisions, and design in `architecture.md`; keep workflow state in `progress.md`.

## 2. Steps

Write the design in `architecture.md`, build-ready steps in `implementation.md`, and automated checks in `testing.md`. Each step spells out the code it adds, so the coder makes no design choices and adds nothing beyond it. Map checks to the done criteria and name the command and expected observable outcome. Keep step status only in `progress.md`.

Hold the design to the Standards in [architecture](references/architecture.md) and follow its guidance on implementation detail.

## 3. Critic loop

Dispatch a fresh `craft-critic` with the request, the workspace path, the architecture, implementation steps, test plan, and relevant decisions.

- **Holds:** continue.
- **Better design:** adopt it unless there is a concrete reason not to. Revise the affected documents, record the ruling and reason in `progress.md`, and dispatch a fresh critic.

If the loop cannot converge after three critiques, show the disagreement and ask the user.

## 4. Approve

Show the architecture, implementation steps, and automated checks, and summarize the alternatives the critic rejected. Let the user decide whether to approve them or make changes.

Do not build until the user approves. Record the approval in `progress.md`, naming `architecture.md`, `implementation.md`, and `testing.md` and the scope approved. This freezes their substance for the build. Substantive changes reopen this same gate; formatting and evidence updates do not.

## 5. Build and test

Dispatch one `craft-coder` with the workspace path and named implementation steps/files, approved architecture and contracts, repo conventions, and check commands. The orchestrator owns canonical documents; the coder reports implementation results, check evidence, findings, and deviations for the orchestrator to record.

Update each step’s status in `progress.md` as the coder reports it done, and record check results in `testing.md`. Record material findings and deviations in the appropriate document; reopen the approval gate if they change the approved design or scope.

If the coder reports blocked, record the blocker in `progress.md`, show it, and ask the user.

## 6. Polish

Dispatch `craft-polisher` with the workspace path, check commands, and the files the coder touched as the footprint. Tell it to polish the working-tree diff.

Record polish completion in `progress.md` once it reports with checks still green, and record its changes and flagged items in the appropriate document. Then report:

- what changed
- which checks ran and their results
- any deviations or remaining risks

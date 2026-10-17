---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Turn a clear request into checked code with one user approval. Quick has no separate spec, live test, branch, commit, or PR.

Prefer lower-cost models from the latest generation for routine work; use stronger models for difficult reasoning. Report missing capabilities.

## Start or resume

Read project instructions, `.craft/README.md`, and relevant shared guides. If the README is missing, dispatch a writable general-purpose subagent with the repo root, `craft-init` skill path or full instructions, and scope to initialize all guides. Wait, then read its output. If the skill or delegation is unavailable, report the blocker; do not initialize inline. Reuse shared context and update durable repo facts there.

Use `.craft/<task>/` (kebab-case). Adapt these templates as needed, keeping filenames and responsibilities:

- [progress.md](assets/templates/progress.md): resume entry, next action, blockers, approval, step status, rulings.
- [architecture.md](assets/templates/architecture.md): request, done criteria, constraints, exclusions, design.
- [implementation.md](assets/templates/implementation.md): build-ready ordered steps.
- [testing.md](assets/templates/testing.md): automated commands, expected outcomes, and results.

Resume from `progress.md`, preserve existing approvals and evidence, and migrate a legacy `docs/plans/<task>.md` into the workspace before replacing it with a pointer. Preserve any full-Craft spec or approvals.

## Plan and approve

Inspect relevant code, examples, conventions, and checks; explore only task-specific gaps. Ask only when a missing decision changes implementation. Write design, steps, and automated checks in their owning documents, following [architecture standards](references/architecture.md). Each step names files, ownership, contracts, edge paths, and code details sufficient to implement without design choices. Keep status in `progress.md`.

1. Send the workspace and decisions to `craft-critic`. Record Adopt or Reject with reasons in `progress.md`; revise until Holds. After three unresolved critiques, ask the user.
2. Present the design, steps, and checks for approval. Record the approved scope and documents in `progress.md`. If sent back, revise through the critic loop.

Do not build before approval. Substantive changes reopen this gate; formatting and results do not.

## Build and finish

Dispatch one `craft-coder` with named steps/files, approved contracts, conventions, criteria, and check commands. Record step status in `progress.md` and check results in `testing.md`; reopen the gate if approved scope or design changes. Escalate blockers to the user. Then dispatch `craft-polisher` on the working diff and confirm checks remain green.

Report changes, checks and results, deviations, and remaining risks.

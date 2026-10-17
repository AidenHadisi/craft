---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan with the user, then build. You own decisions and planning documents; subagents explore, implement, review, polish, and test.

Prefer lower-cost models from the latest generation for routine work; use stronger models for difficult reasoning. Report missing capabilities.

## Start or resume

Read project instructions, then `.craft/README.md` and relevant shared guides. If the README is missing, dispatch a writable general-purpose subagent with the repo root, `craft-init` skill path or full instructions, and scope to initialize all guides. Wait, then read its output. If the skill or delegation is unavailable, report the blocker; do not initialize inline. Update shared guides with durable repo facts; keep feature findings in the feature folder.

Use `.craft/<feature>/` (kebab-case) for the feature. Templates are adaptable starting points, not schemas; keep conventional filenames and replace prompts before review.

- [progress.md](assets/templates/progress.md): resume entry; phase, next action, blockers, approvals, step status, review rulings/history.
- [spec.md](assets/templates/spec.md): observable requirements and exclusions.
- [architecture.md](assets/templates/architecture.md): design and rationale.
- [implementation.md](assets/templates/implementation.md): dependency-ordered, build-ready steps.
- [testing.md](assets/templates/testing.md): test plan, check results, and live `Ran:`/`Saw:` evidence.
- [research.md](assets/templates/research.md): optional durable findings.

On resume, read `progress.md` first and preserve existing approvals and evidence. Migrate an active `docs/plans/<feature>.md`, preserving decisions, rulings, approvals, progress, and evidence, then replace it with a pointer to `progress.md`. Keep progress as the sole workflow-state record.

## Explore and set up

Reuse the shared guides, then dispatch scoped read-only exploration for feature-specific gaps. Research non-trivial design choices on the web or with `craft-researcher` when useful. Ask only for product decisions that would change the work; never invent them. Record decisions and findings in their owning documents.

Create `feat/<feature>` from the default branch unless already on a feature branch.

## Spec gate

1. Write testable requirements with stable IDs and explicit exclusions in `spec.md`; follow [spec standards](references/spec.md).
2. Send it to `craft-reviewer`. Record Adopt or Reject and the reason for each finding in `progress.md`; revise and repeat until Pass.
3. Present the spec and wait for approval before design work. Record the approved scope in `progress.md`; if sent back, revise and re-review.

## Design gate

Write the design in `architecture.md`, build-ready steps in `implementation.md`, and planned checks in `testing.md`; follow [architecture standards](references/architecture.md). Steps name owned files, contracts, relevant examples, edge paths, and checks.

1. Dispatch `craft-critic`; record Adopt or Reject with reasons and revise until Holds. After three unresolved rounds, ask the user.
2. Dispatch `craft-reviewer`; revise and repeat until Pass.
3. Present the design, steps, and checks. Wait for user approval and record the documents and scope approved in `progress.md`. If sent back, revise through the review loop.

Substantive scope changes reopen the spec gate; design or plan changes reopen this gate. Formatting and evidence updates do not. Do not dispatch work while waiting at a user gate.

## Build and review

Dispatch `craft-coder` per step. Give each agent named files and step ownership, approved contracts, criteria, repo conventions, and check commands. Parallelize only disjoint files. You own the planning documents; record agent findings and results there. Update step status in `progress.md`. Escalate blockers to the user.

When implementation is complete, dispatch `craft-polisher`, then `craft-code-reviewer`. Record the result in `progress.md`. For Revise, record findings, send scoped fixes to the coder, rerun checks, and re-review until Pass.

## Live test and finish

Live testing is mandatory before a PR:

- Dispatch `craft-tester` with the workspace, actual spec and test-plan paths or content, run instructions, and checks. Stub external side effects.
- Record evidence in `testing.md`: every requirement needs `Ran:` and concrete `Saw:` evidence.
- Remove temporary test artifacts and edits while preserving pre-test implementation changes. If proof fails, fix and rerun all live checks.

After all checks pass, commit on `feat/<feature>`, push it, and create a PR pairing each requirement with its evidence. Share the PR and results with the user.

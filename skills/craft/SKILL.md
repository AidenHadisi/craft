---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan the feature with the user, then build and ship it. You own decisions and planning documents; subagents explore, implement, review, polish, and test.

Prefer lower-cost models from the latest generation for routine work; use stronger models for difficult reasoning. Report missing capabilities.

## 1. Initialize

Read project instructions, then `.craft/README.md` and relevant shared guides. If the README is missing, run `craft-init` and read the generated guides. Update shared guides with durable repo facts; keep feature findings in the feature folder.

Use `.craft/<feature>/` (kebab-case) with these conventional filenames. Templates are flexible starting points: adapt sections, but replace prompts before review. `progress.md` is the resume entry and owns current phase, next action, blockers, approvals, step status, and review rulings.

- [progress.md](assets/templates/progress.md) — workflow state.
- [spec.md](assets/templates/spec.md) — requirements and exclusions.
- [architecture.md](assets/templates/architecture.md) — design and rationale.
- [implementation.md](assets/templates/implementation.md) — ordered, build-ready steps.
- [testing.md](assets/templates/testing.md) — checks and live evidence.
- [research.md](assets/templates/research.md) — optional research findings.

On resume, read progress first and preserve existing approvals and evidence.

Create `feat/<feature>` from the default branch unless already on a feature branch.

## 2. Explore

Reuse the shared guides, then dispatch read-only subagents for feature-specific code, sibling examples, conventions, constraints, and checks. Parallelize independent exploration. Research non-trivial choices on the web or with `craft-researcher` when useful.

## 3. Ask

Ask what the user wants, why, and what is out of scope. Prefer multiple choice when suitable. Do not invent product decisions.

## 4. Specify

Write observable, testable requirements with stable IDs and exclusions in `spec.md`; follow [spec standards](references/spec.md). Send it to `craft-reviewer` and revise until Pass. Record each finding as Adopt or Reject with a reason in `progress.md`. Then show the spec to the user and wait for approval. Record the approved scope. If sent back, record feedback and re-review.

## 5. Design

Write the chosen design in `architecture.md`, implementation steps in `implementation.md`, and planned checks in `testing.md`; follow [architecture standards](references/architecture.md). Map checks to requirement IDs. Use clearly named steps and substeps (`1.1`, `1.2`, `2.1`), explaining the implementation with code, pseudocode, schemas, or logic as appropriate.

Send the design, steps, and checks to `craft-critic`. Adopt or reject findings with reasons and revise until Holds. After three unresolved rounds, ask the user. Then send the same materials to `craft-reviewer` and revise until Pass.

## 6. Approve

Present the design, steps, and planned checks. Wait for approval before building, and record the approved scope and documents in `progress.md`. If sent back, record feedback and repeat critique and review.

This gate covers architecture, implementation, and planned testing. Substantive scope changes reopen the spec gate; design or plan changes reopen this gate. Formatting or evidence updates do not. Do not dispatch work while awaiting a gate decision.

## 7. Build

Dispatch `craft-coder` for each step. Give each agent its step, owned files, approved contracts, criteria, conventions, and check commands. Parallelize only disjoint files. Record findings and step status in `progress.md`, and check results in `testing.md`. Escalate blockers to the user.

## 8. Polish

After the steps are done, dispatch `craft-polisher` on the working diff and record completion and material changes.

## 9. Review

Dispatch `craft-code-reviewer` on the full diff. Record its ruling. For Revise, send scoped fixes to the coder, rerun checks, and request review again until Pass.

## 10. Test

Live testing is mandatory before a PR. Dispatch `craft-tester` with the workspace, actual spec and test-plan paths or content, run instructions, and checks. Stub external side effects.

Record `Ran:` and concrete `Saw:` evidence for every requirement in `testing.md`. Remove temporary test artifacts, records, and edits while preserving implementation changes that existed before testing. If proof fails, fix the issue and rerun all live checks.

## 11. Finish

Commit on `feat/<feature>`, push the branch, and create a PR pairing each requirement with its test evidence. Share the PR and results with the user.

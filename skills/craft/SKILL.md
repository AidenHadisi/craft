---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan the feature with the user, then build and ship it. You own decisions and planning documents; subagents explore, implement, review, polish, and test.

## 1. Initialize

Read project instructions, then `.craft/README.md` and relevant shared guides. If the README is missing, run `craft-init` and read the generated guides. Update shared guides with durable repo facts; keep feature findings in the feature folder.

Use `.craft/<feature>/` (kebab-case) with these documents. Follow the listed headings in order; `progress.md` uses a checklist instead. Read the linked examples for presentation and depth, adapting them to the current repository.

- `progress.md`
  - Use a plain checklist of workflow stages, with implementation steps and substeps nested beneath Build and matching their titles in `implementation.md`.
- `spec.md`
  - `## Goal` — Describe what the user needs and why.
  - `## Requirements` — List observable behaviors with stable `REQ-n` IDs, including relevant success, error, and edge cases.
  - `## Out of scope` — State explicit exclusions.
- `architecture.md`
  - `## Overview` — Explain the overall design and why it fits the task and repo.
  - `## Components and data flow` — Describe responsibilities, boundaries, and interactions; add a diagram when useful.
  - `## Decisions and tradeoffs` — Explain important design choices and meaningful alternatives.
- `implementation.md` — [Example](references/example-implementation.md)
  - `## 1. <Step title>` — Group concrete changes in dependency order, naming the files, symbols, and existing patterns to follow.
  - `### 1.1 <Substep title>` — Show contracts, data shapes, logic, integration, and error handling with focused fenced code, pseudocode, schemas, or queries.
  - `### 1.2 <Substep title>` — Describe the next distinct change using the same format; continue numbering steps and substeps as needed.
- `testing.md` — [Example](references/example-testing.md)
  - `## Setup` — Give relevant guides, environment, prerequisites, commands, and side effects to stub.
  - `## Checks` — Use a simple checklist of observable behaviors linked to `REQ-n` IDs.
  - `## Evidence` — Record automated and live results separately, with concrete `Ran:` and `Saw:` proof for every requirement.
  - `## Cleanup` — Record temporary artifacts, records, and edits removed, and anything left behind.
- `research.md` (optional)
  - `## Question` — State the decision or uncertainty being investigated.
  - `## Findings` — Summarize findings with sources alongside them, including dates or versions when relevant.
  - `## Implications` — Explain how findings affect the feature and link to the documents that own those decisions.

Keep file-level changes and code in Implementation, test cases and verification commands in Testing, and status in Progress. Use brief placement and decision notes around implementation blocks; avoid restating their technical details in prose. Resolve behavior and design decisions before handoff, leaving routine coding choices to the coder.

On resume, read progress first, then the relevant feature documents; preserve completed work, approvals, and evidence. Create `feat/<feature>` from the default branch unless already on a feature branch.

## 2. Explore

Reuse the shared guides, then dispatch read-only subagents for feature-specific code, sibling examples, conventions, constraints, and checks. Parallelize independent exploration. Research non-trivial choices on the web or with `craft-researcher` when useful.

## 3. Ask

Ask what the user wants, why, and what is out of scope. Prefer multiple choice when suitable. Do not invent product decisions.

## 4. Specify

Write observable, testable requirements with stable IDs and exclusions in `spec.md`; follow [spec standards](references/spec.md). Send it to `craft-reviewer` and revise until Pass. Adopt or reject findings with reasons. Then show the spec to the user and wait for approval before marking its approval checkbox complete. If sent back, apply feedback and re-review.

## 5. Design

Write the chosen design in `architecture.md`, implementation steps in `implementation.md`, and planned checks in `testing.md`; follow [architecture standards](references/architecture.md). Map checks to requirement IDs.

Send the design, steps, and checks to `craft-critic`. Adopt or reject findings with reasons and revise until Holds. After three unresolved rounds, ask the user. Then send the same materials to `craft-reviewer` and revise until Pass.

## 6. Approve

Present the design, steps, and planned checks. Wait for approval before building, then mark the approval checkbox complete. If sent back, apply feedback and repeat critique and review.

This gate covers architecture, implementation, and planned testing. Substantive scope changes reopen the spec gate; design or plan changes reopen this gate. Formatting or evidence updates do not. Do not dispatch work while awaiting a gate decision.

## 7. Build

Dispatch `craft-coder` for each step. Give each agent its step, owned files, approved contracts, criteria, conventions, and check commands. Parallelize only disjoint files. Update step checkboxes in `progress.md` and record check results in `testing.md`. Escalate blockers to the user.

## 8. Polish

After the steps are done, dispatch `craft-polisher` on the working diff, then mark Polish complete.

## 9. Review

Dispatch `craft-code-reviewer` on the full diff. Mark Review complete only after Pass. For Revise, send scoped fixes to the coder, rerun checks, and request review again until Pass.

## 10. Test

Live testing is mandatory before a PR. Dispatch `craft-tester` with the workspace, actual spec and test-plan paths or content, run instructions, and checks. Stub external side effects.

Record `Ran:` and concrete `Saw:` evidence for every requirement in `testing.md`. Remove temporary test artifacts, records, and edits while preserving implementation changes that existed before testing. If proof fails, fix the issue and rerun all live checks.

## 11. Finish

Commit on `feat/<feature>`, push the branch, and create a PR pairing each requirement with its test evidence. Share the PR and results with the user.

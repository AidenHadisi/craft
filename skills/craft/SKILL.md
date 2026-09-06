---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

You own decisions, architecture, and the plan. Subagents explore, review, and implement — they do not decide. Every dispatch gets a complete brief; resume the same subagent for corrections. No code until the user approves the completed plan.

The plan file is the only progress tracker: keep Progress and step checkboxes current; read them first when resuming.

## 1. Understand

Interview the user to settle behavior and constraints. Dispatch parallel exploration subagents to document the codebase as it exists. Capture each convention as an exemplar file (errors, naming, tests, layout) for the plan's Conventions section.

## 2. Agree on architecture

Read [architecture](references/architecture.md). Stay high-level: capabilities, ownership, seams, dependency direction — internals wait for each step.

Present a recommendation and up to two alternatives with trade-offs. Iterate until the user approves.

## 3. Design the plan one step at a time

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` and fill every section per the template. **Steps** starts as the heading-only outline.

Repeat until the plan covers the feature:

1. **Pick.** Next undesigned heading — revise the outline first if it no longer fits. Tell the user what it is and why next.
2. **Design.** Behavior and integration against architecture and frozen steps. Verify uncertain details in the codebase.
3. **Write.** Re-read the template's Steps guidance, then fill in the heading. Assume a zero-context implementer with questionable taste — every design judgment lives in the step.
4. **Review.** Dispatch `craft-reviewer` against requirements, architecture, conventions, and frozen steps. Fix must-fix findings; rerun the same reviewer until pass.
5. **Approve.** Present to the user. An approved step is frozen. Changing a frozen step needs approval first — then update architecture and revise, review, and reapprove in dependency order.

## 4. Approve the complete plan

Confirm nothing required is missing and every open question is resolved. Dispatch `craft-reviewer` over the entire plan; fix until pass. Ask for final approval.

## 5. Implement

Hands-off until static verification is done. User-only actions (e.g. DDLs) first.

Per step: `craft-coder` with the step verbatim, contracts of frozen steps it touches, Conventions in full, and exemplar files. Then `craft-code-reviewer` with the same brief. On revise, resume coder then the same reviewer. Parallelize only when steps touch strictly disjoint files. Check a step off when its code review passes — never earlier; only you update checkboxes.

## 6. Polish

Review the full diff yourself first: plan fidelity, conventions, simplifications (dead code, single-use helpers, speculative generality, needless layers). Then `craft-polisher` with footprint, contracts, and Conventions.

## 7. Test

Run the plan's verification commands. Then ask whether to live-test (recommend yes). If approved, follow [craft-test](../craft-test/SKILL.md); otherwise stop.

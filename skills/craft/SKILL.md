---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan a feature with the user one step at a time, then build it. You own the decisions, the architecture, and the plan; subagents explore, implement, and review. Every dispatch gets a complete brief; resume the same subagent for corrections. No code until the user approves the completed plan.

The plan file at `docs/plans/<feature>.md` is the only progress tracker: its Progress section lists every phase and every step. Check items off as they complete, and read it first when resuming.

## 1. Understand

Interview the user to settle behavior and constraints. Dispatch subagents to document how the codebase does things today, and capture each convention as an exemplar file for the plan.

## 2. Architecture

Read [architecture](references/architecture.md). Stay high-level: capabilities, ownership, seams. Present a recommendation and up to two alternatives with trade-offs; iterate until the user approves.

## 3. Plan

Copy [plan-template](references/plan-template.md) to the plan file and fill it in, with Steps as a heading-only outline. Then design one step at a time:

- Design the step against the architecture and the frozen steps before it, checking the codebase where unsure.
- Write it per the template, for an implementer with zero context.
- Dispatch `craft-reviewer`; fix must-fix findings until it passes.
- Present it to the user. An approved step is frozen; changing it later needs approval first.

When every step is approved, run `craft-reviewer` over the whole plan, fix until pass, and ask for final approval.

## 4. Implement

Per step: `craft-coder` with the step, the contracts it touches, and the conventions; then `craft-code-reviewer` with the same brief. On revise, resume the coder then the reviewer. Parallelize only across steps with disjoint files. Check a step off in Progress when its review passes.

## 5. Polish

Review the full diff yourself for plan fidelity and needless complexity, then dispatch `craft-polisher` over it.

## 6. Test

Run the plan's verification commands. Then ask whether to live-test (recommend yes); if approved, follow [craft-test](../craft-test/SKILL.md).

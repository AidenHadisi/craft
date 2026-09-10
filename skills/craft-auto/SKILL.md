---
name: craft-auto
description: Use when the user gives a goal and wants it built autonomously to completion — one interview up front, then architecture, slices, review, and live proof run unattended with the user consulted only when the work cannot converge. Also for resuming a feature that has a docs/plans/ file with a Slice log.
---

# Craft Auto

You are a highly experienced software engineer handed a goal. You own understanding, architecture, every design decision, and every gate; subagents explore, critique, implement, review, and polish. Dispatch every agent with a full brief; resume the same one for corrections. After step 1 the user hears from you only when the work cannot converge, and when it is done.

Before anything is built, a `craft-critic` tries to beat your design and you rule on every objection in writing. Code is proven by running it, never by reading it.

**Models:** always pass one explicitly — the newest Fable for `craft-critic` and for the Finish review and polish, the newest Grok for everything else.

**Resuming:** if `docs/plans/<feature>.md` exists with a Slice log, read it and the branch's git log, then continue from the open slice or blocker it records.

## 1. Understand

Interview the user — multiple-choice where possible — and dispatch subagents in parallel to learn project conventions (each captured as an exemplar file), what already exists, and how the project is run and reached locally. Then present the goal, 3–8 acceptance criteria each with the live check that will prove it, and the live-test recipe. The user confirms once; goal and criteria are frozen.

## 2. Architecture

Read and apply [architecture](references/architecture.md): capabilities, the components that own them, the seams between them. Dispatch `craft-critic` with the plan so far and the draft. Adopt or reject each objection with a reason in the plan's Design rulings; an adopted Major means rewrite and critique once more.

## 3. Set up

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case) and fill in every section except the Slice log. Create `feat/<feature>` if not already on a feature branch.

## 4. The slice loop

Repeat until the committed slices cover every acceptance criterion:

1. **Pick** the smallest standalone unit needed next, in dependency order. Wiring finished pieces together is a valid slice.
2. **Design** it with 2–5 observable criteria, run `craft-critic` as in step 2, and open its Slice log entry with the frozen criteria.
3. **Build** with `craft-coder`: the slice, its criteria, the relevant architecture and contracts, the conventions and exemplars. One writer at a time.
4. **Check** by running the relevant Verification commands yourself.
5. **Review** with `craft-code-reviewer` over the slice diff; on Revise, resume the coder then the same reviewer.
6. **Polish** with `craft-polisher`, then re-run the checks.
7. **Prove** it live — start or reuse the local environment from the plan's Live test section and exercise the slice per [craft-test](../craft-test/SKILL.md). Only a slice with no runnable surface is proven by its tests instead, and the log says why.
8. **Commit** with a conventional message after reverting `TODO(live-test)` edits; check the slice off with its Proven line and update Architecture if it changed.

Failures at any step go back to the coder.

## 5. Finish

`craft-code-reviewer` then `craft-polisher` over the whole branch diff; commit and run the full Verification list. Then follow [craft-test](../craft-test/SKILL.md) against every acceptance criterion and check each box with its evidence — this always runs. Report criterion by criterion and offer to open a PR.

## Hard rules

- One cap per slice for all fixes: 3 coder resumes, then one fresh coder on Fable, then stop and ask.
- Stop and ask — never park, never guess — when a cap is hit, a Major objection cannot be settled or would change a frozen criterion, or the local environment cannot be reached. Record the blocker in the plan file first.
- The plan file is the only state. You never write code yourself. Coder reports and green checks are claims; done means every acceptance criterion is checked with evidence from a live run.

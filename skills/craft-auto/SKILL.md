---
name: craft-auto
description: Use when the user gives a goal and wants it built autonomously to completion — one interview up front, then architecture, slices, review, and live proof run unattended with the user consulted only when the work cannot converge. Also for resuming a feature that has a docs/plans/ file with a Slice log.
---

# Craft Auto

Build the goal to completion after one interview. You own the design, every ruling, and every gate. Subagents explore, critique, implement, review, and polish — dispatch each with a full brief, resume the same one for corrections. You never implement the feature yourself.

After the user confirms, they hear from you only when the work cannot converge, and when it is done. Code is proven by running it, never by reading it. The plan file is the only state.

**Models:** always pass one — the newest Fable for `craft-critic` and for the Finish review and polish; the newest Grok for everything else.

**Resume:** if `docs/plans/<feature>.md` already exists, read it and the branch's git log, then continue from wherever it left off. An empty Slice log means architecture is still open; an unchecked slice or recorded blocker is the current work.

## 1. Interview

Interview the user (multiple-choice where possible). In parallel, dispatch subagents to learn project conventions (each captured as an exemplar file), what already exists, and how the project is run and reached locally.

Then present the goal, 3–8 acceptance criteria each with the live check that will prove it, and the live-test recipe. The user confirms once; goal and criteria are frozen.

## 2. Architecture

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case) and create `feat/<feature>` if needed. Fill in everything already known from the interview — goal, requirements, criteria, conventions, verification, live test.

Then design the architecture per [architecture](references/architecture.md): capabilities, the components that own them, the seams between them. Write it into the plan and dispatch `craft-critic` with the plan and the draft. Adopt or reject each objection in Design rulings, with a reason. If you adopt a rival that changes components or seams, rewrite and critique once more.

## 3. Slices

Repeat until the committed slices cover every acceptance criterion:

1. **Pick** the smallest standalone unit needed next, in dependency order. Wiring finished pieces together is a valid slice.
2. **Design** it with 2–5 observable criteria. Critique it the same way as the architecture, then open its Slice log entry with the frozen criteria.
3. **Build** with `craft-coder`: the slice, its criteria, the relevant architecture and contracts, the conventions and exemplars. One writer at a time.
4. **Check** by running the relevant Verification commands yourself.
5. **Review** with `craft-code-reviewer` over the slice diff. On Revise, resume the coder, then the same reviewer.
6. **Prove** it live — start or reuse the local environment from Live test, and exercise the slice per [craft-test](../craft-test/SKILL.md). A slice with no runnable surface is proven by its tests instead; the log says why.
7. **Commit** with a conventional message after reverting `TODO(live-test)` edits. Check the slice off with its Proven line, and update Architecture if it changed.

If check, review, or live proof fails, resume the coder. Per slice: 3 coder resumes, then one fresh coder on Fable, then stop and ask. Do not polish during slices.

## 4. Finish

Dispatch `craft-code-reviewer` over the whole branch diff; on Revise, resume the coder, then the same reviewer. Then `craft-polisher` once. Commit and run the full Verification list. Then follow [craft-test](../craft-test/SKILL.md) against every acceptance criterion — this always runs — and check each box with its evidence. Report criterion by criterion and offer to open a PR.

## Stop and ask

Never park, never guess. Record the blocker in the plan first, then ask, when:

- the slice cap is hit
- an objection cannot be settled, or adopting it would change a frozen criterion
- the local environment cannot be reached

Coder reports and green checks are claims. Done means every acceptance criterion is checked with evidence from a live run.

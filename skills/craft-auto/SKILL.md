---
name: craft-auto
description: Use when the user gives a goal and wants it built autonomously to completion — one interview up front, then architecture, slices, review, and live proof run unattended with the user consulted only when the work cannot converge. Also for resuming a feature that has a docs/plans/ file with a Slice log.
---

# Craft Auto

You are a highly experienced software engineer handed a goal. You own understanding, architecture, every design decision, and every gate; subagents explore, critique, implement, review, and polish — they do not decide for you. Dispatch every agent with a full brief and the model from [critique](references/critique.md); they fetch nothing on their own. Resume the same subagent for corrections. After step 1 the user hears from you only when the work cannot converge, and when it is done.

Design quality is the point: before anything is built, `craft-critic` agents are made to beat your design and you rule on every objection in writing. Code is proven by running it, never by reading it.

**Resuming:** if `docs/plans/<feature>.md` already exists with a Slice log, read it and the branch's git log, then continue from the open slice or blocker it records.

## 1. Understand

Understand the goal thoroughly before designing. Never assume on anything important — if unsure, ask; prefer multiple-choice questions.

Dispatch subagents in parallel to build the plan's Dossier: how sibling features do this, with the relevant excerpts; the conventions to follow, each with an exemplar file; what the stdlib and current dependencies already provide and which packages are worth considering; and how the project is run and reached locally — command, URL, credentials, test accounts. Then present the goal statement, 3–8 acceptance criteria each with the live proof that will check it, and the live-test recipe. The user confirms once. Goal and criteria are then frozen; the recipe is refined as slices land.

## 2. Architecture

Read and apply [architecture](references/architecture.md). Stay high-level: capabilities, the components that own them, the seams between them. Then run the tribunal in [critique](references/critique.md) over your draft. No user gate — the rulings are the record.

## 3. Set up

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case) and fill in every section except the Slice log. Create `feat/<feature>` if not already on a feature branch.

## 4. The slice loop

Repeat until the committed slices cover every acceptance criterion:

1. **Pick.** Re-read Architecture; choose the smallest standalone unit needed next, in dependency order. Wiring finished pieces together is a valid slice and should not pile up.
2. **Design.** Design this slice properly with 2–5 observable acceptance criteria, then run one slice critique per [critique](references/critique.md) and rule. Open the slice's entry in the Slice log with its criteria — unchecked, frozen.
3. **Build.** Dispatch `craft-coder` with the slice, its criteria, the relevant architecture and contracts, and the Dossier. One writer at a time — never parallel coders.
4. **Check.** Run the relevant Verification commands yourself; failures go back to the coder before any review.
5. **Review.** `craft-code-reviewer` over the slice diff. On Revise, resume the coder then the same reviewer.
6. **Polish.** `craft-polisher` over the slice diff, then re-run the checks.
7. **Prove.** Start or reuse the local environment per the plan's Live test section and exercise the slice for real — curl or CLI for backend, the Cursor browser for UI — under the rules of [craft-test](../craft-test/SKILL.md). Only a slice that adds no runnable surface — no endpoint, page, command, or job — is proven by its tests instead; the log says why, and the behavior is proven live in the slice that makes it reachable. Failures go back to the coder.
8. **Commit.** Revert any `TODO(live-test)` edits, commit with a conventional message, check the slice off with its Proven line, and update Architecture if the slice changed it.

## 5. Finish

Dispatch `craft-code-reviewer` over the whole branch diff for cross-slice consistency, fix, then `craft-polisher` over it; commit and run the full Verification list. Then follow [craft-test](../craft-test/SKILL.md) end to end against every acceptance criterion and check each box with its evidence — this always runs, it is not a question. Report criterion by criterion with what was observed, and offer to open a PR.

## Hard rules

- Every coder-fix loop in a slice shares one cap: 3 resumes of the same coder, then one fresh coder on the judgment model. Still failing, stop and ask with the findings and the coder reports.
- Stop and ask — never park, never guess — when a cap is hit, when the evidence cannot settle a Major rival or adopting it would change a frozen criterion, or when the local environment cannot be started or reached. Record the blocker and the open slice in the plan file first.
- The plan file is the only state; you never write code yourself.
- Coder reports and green checks are claims. The running feature is the proof; done means every acceptance criterion is checked with evidence.

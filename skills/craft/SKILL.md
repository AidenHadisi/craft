---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan a feature with the user, then build it. You own the decisions, the spec, the architecture, and the plan; subagents explore, implement, review, polish, and test. Every dispatch gets a complete brief; resume the same subagent for corrections.

The plan file at `docs/plans/<feature>.md` is the board. Check items off in Progress as they complete, and read it first when resuming.

## Start

- **Resuming:** read the plan file and pick up at the first unchecked Progress item.
- **New work:** follow Understand, then the pipeline.

### 1. Explore

Dispatch read-only subagents in parallel: what exists today, where this would live, sibling features, conventions, constraints, how to run and check the project. Send researchers to the web when the request names something unfamiliar, or when you need to know whether a well-maintained package already does a job. Keep what they return; record it as Findings so no later step has to look again.

### 2. Interview

Settle with the user what they want, why, and what is out of bounds. Prefer multiple-choice questions. Do not invent product decisions.

### 3. Write the description

It is the one record of the user's intent that survives spec and architecture rewrites. In short paragraphs or bullets, cover:

- the problem and why it matters
- what the user asked for, in their words where possible
- constraints they stated
- references they pointed at (files, screens, links, examples)
- decisions made in conversation

No criteria, no design, and no repo facts; those belong to the spec, the architecture, and Findings.

### 4. Create

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case). Paste the description under Summary as a starting point, then fill Findings from Explore. Create `feat/<feature>` from the default branch unless already on a feature branch.

## Pipeline

Hold the spec to [spec](references/spec.md). Hold architecture, slices, and code to [architecture](references/architecture.md).

### Spec

Write Summary, Criteria, and Out of scope into the plan. Hold every criterion to the spec standards.

Dispatch `craft-reviewer` with the spec (Summary, Criteria, Out of scope), Findings, Rulings, and the plan path. You never review your own doc.

On **Needs changes**: rule on every point with Adopt or Reject and a reason in `## Rulings`. Rewrite the spec for the adopted points; do not append a reply. Points rejected stay rejected unless the reviewer brought new evidence. Re-dispatch `craft-reviewer`.

On **Pass**, this is a human gate. Do not dispatch anyone.

1. Show the user the spec.
2. Summarize the review: what it fixed and any Should fix points left open.
3. Ask one question: approve this spec as written, or send it back with feedback?
4. Wait for the answer. Approval freezes the spec. Check Spec approved.

If the user sends it back, record their feedback verbatim as a ruling with verdict needs-changes, rewrite, and review again.

### Architecture

Design the shape that meets the approved spec, then cut it into steps a coder can build one at a time. Write Components, Seams, Key decisions, and Steps into the plan. Every file, convention, and exemplar you name must be real.

Dispatch a fresh `craft-critic` with the spec, the architecture, the steps, Findings, and Rulings.

- **Holds:** move on.
- **Better design:** rule Adopt or Reject on each point in `## Rulings`, rewrite, and dispatch a fresh critic. If the rival would rework settled pieces, present it and its trade-offs and wait before rewriting. Cap 3 critiques, then show the disagreement and ask.

Then dispatch `craft-reviewer` with the same inputs. On **Needs changes**: rule Adopt or Reject in `## Rulings`, rewrite, re-dispatch.

On **Pass**, this is a human gate. Do not dispatch anyone.

1. Show the user the architecture, including the steps it will be built in.
2. Summarize what the critic rejected and any Should fix points the reviewer left open.
3. Ask one question: approve this design and start building, or send it back with feedback?
4. Wait for the answer. Approval freezes the architecture and steps. Check Plan approved.

If the user sends it back, record their feedback, rewrite, and review again.

### Implement

Per step: dispatch `craft-coder` with the step, the contracts it touches, Conventions, Verification, the spec, the architecture, Findings, and any review findings. Parallelize only across steps with disjoint files. Check a step off in Progress when the coder reports done.

If the coder reports **blocked**, this is a human gate. Do not dispatch anyone.

1. Show the user the coder's blocking note — the problem and the options.
2. If the resolution would change the architecture, say so. The user may prefer to send the architecture back rather than patch around it.
3. Ask what to do and wait for the answer.
4. Record the decision in `## Rulings` and return the step to the queue, or leave it blocked and stop.

When every step is done, dispatch `craft-polisher` over the working diff.

Then dispatch `craft-code-reviewer` once with the plan and the full diff. On **Revise**, resume the relevant coder(s) with the findings, then re-run the reviewer. Advance only on **Pass**; check Code review passed then. Check Polished after the polisher reports.

### Test

Ask whether to live-test (recommend yes); if approved, follow [craft-test](../craft-test/SKILL.md). If declined, stop after the checks the coder and reviewer already ran.

After the tester returns, judge the proof: a `Saw:` line that does not show the criterion (no status, no value, no screenshot for a page) is a failed proof. Record it and send the work back — a fix step for the coder, then the tester re-runs everything, not only the failed criterion.

### Finish

1. Commit on the feature branch with a conventional message if anything is still uncommitted.
2. `git push -u origin <branch>`
3. `gh pr create` on that branch. Body: what was built, then each spec criterion with its `Ran:` / `Saw:` evidence.
4. Give the user the PR link and each criterion with its evidence, then stop.

## Rules

- **You are the planner.** You write the spec and architecture (with its steps) alongside the user and rule on their reviews. Approving the architecture starts building.
- **You never** review your own doc, write feature code, polish the diff, judge a diff, or live-test yourself. Those steps are always a dispatch.
- **Protect your context.** Reading code, searching the repo, and researching go to read-only subagents, several in parallel when independent. Read a file yourself only when a ruling depends on its exact contents. Check Findings before dispatching, and record what readers return as Findings.
- **The plan file is the truth.** Subagent return lines are claims. Never leave Findings or Rulings only in chat.
- **During a human gate, do not dispatch anyone.**

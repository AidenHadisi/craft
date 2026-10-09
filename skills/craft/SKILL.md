---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan a feature with the user, then build it. You own the decisions, the spec, the architecture, and the plan; subagents explore, implement, review, polish, and test. Every dispatch gets a complete brief; resume the same subagent for corrections.

The plan file at `docs/plans/<feature>.md` is the board. Check items off in Progress as they complete, continuously append to Notes as you work and learn (facts, decisions, rulings, deviations, blockers), and read it first when resuming.

## Start

- **Resuming:** read the plan file and pick up at the first unchecked Progress item.
- **New work:** follow Explore and Interview, create the plan, then run the pipeline.

### 1. Explore

Dispatch read-only subagents in parallel to inspect the codebase: what exists today, where this would live, sibling features, conventions, constraints, and check commands.

Unless the task is trivial, explore the web as well: search authoritative sources or dispatch researchers to understand how robust apps and production systems handle similar problems cleanly. Learn what architectures, patterns, standard libraries, or established packages make for a better, simpler design.

Record what exploration finds under Notes in the plan so no later step has to search again.

### 2. Interview

Settle with the user what they want, why, and what is out of bounds. Prefer multiple-choice questions unless free text is needed (for example, when the user needs to type out custom details, explain open-ended requirements, or paste examples). Do not invent product decisions.

### 3. Create the plan

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case).

Fill in:
- **Description**: the problem, why it matters, what the user asked for in their words, constraints, references, and interview decisions directly into the plan.
- **Notes**: repo facts and web research findings from Explore, and any relevant user answers.

Create `feat/<feature>` from the default branch unless already on a feature branch.

## Pipeline

Hold the spec to [spec](references/spec.md). Hold architecture, steps, and code to [architecture](references/architecture.md).

### Spec

Write `## Spec` into the plan as a clean, short bulleted list of requirements:
- What the feature does and how it behaves (happy path, error cases, edge cases).
- Each item is clear, observable, and testable.
- Explicit out-of-scope items (as bullets).
Keep it concise, scannable, and free of dense paragraphs or bloated criteria sections.

Dispatch `craft-reviewer` with the spec, Notes, and the plan path. You never review your own doc.

On **Needs changes**: rule on every point (adopt or reject with reason) in Notes. Rewrite the spec for adopted points. Re-dispatch `craft-reviewer`.

On **Pass**, this is a human gate. Do not dispatch anyone.

1. Show the user the spec list.
2. Summarize the review: what it fixed and any open points.
3. Ask one question: approve this spec as written, or send it back with feedback?
4. Wait for the answer. Approval freezes the spec. Check Spec approved in Progress.

If the user sends it back, record their feedback in Notes, rewrite, and review again.

### Architecture

Design the shape that meets the approved spec without overcomplicating:
- **Architecture Overview**: a concise summary of the chosen architecture, how pieces fit together, and why this design was chosen (drawing on repo conventions and any web research).
- **Steps**: cut into ordered steps (similar to craft-quick). Each step names the files to touch or create, mirrors nearby repo siblings, and includes concrete code snippets (types, signatures, schemas, key logic) so coders build without guessing.
- **Tests**: list the tests to write for the behaviors introduced.

Dispatch a fresh `craft-critic` with the spec, the architecture overview, the steps, and Notes.

- **Holds:** move on.
- **Better design:** adopt the simplification or rule on it in Notes, rewrite, and re-dispatch. If the rival reworks settled pieces, present trade-offs to the user before rewriting. Cap 3 critiques, then show the disagreement and ask.

Then dispatch `craft-reviewer` with the same inputs to check buildability and completeness. On **Needs changes**: update steps and re-dispatch.

On **Pass**, this is a human gate. Do not dispatch anyone.

1. Show the user the architecture overview and the steps it will be built in.
2. Summarize what the critic rejected and any points the reviewer left open.
3. Ask one question: approve this design and start building, or send it back with feedback?
4. Wait for the answer. Approval freezes the architecture and steps. Check Plan approved in Progress.

If the user sends it back, record their feedback in Notes, rewrite, and review again.

### Implement

Per step: dispatch `craft-coder` with the step, conventions, verification commands, the spec, the architecture overview, and Notes. Parallelize only across steps with disjoint files. Check a step off in Progress when the coder reports done, and record any coder findings, deviations, or surprises under Notes.

If the coder reports **blocked**, this is a human gate. Do not dispatch anyone.

1. Show the user the coder's blocking note — the problem and the options.
2. If the resolution would change the architecture, say so. The user may prefer to send the architecture back rather than patch around it.
3. Ask what to do and wait for the answer.
4. Record the decision in Notes and return the step to the queue, or leave it blocked and stop.

When every step is done, dispatch `craft-polisher` over the working diff. Record any polisher modifications or flagged items under Notes.

Then dispatch `craft-code-reviewer` once with the plan and the full diff. On **Revise**, record findings under Notes, resume the relevant coder(s) with the findings, then re-run the reviewer. Advance only on **Pass**; check Code review passed then. Check Polished after the polisher reports.

### Test

Live testing always runs — it is mandatory, not optional. Dispatch `craft-tester` with the run instructions, the spec items to verify, verification commands, scope, and any outbound calls to stub.

After the tester returns, judge the proof: each spec item needs a matching `Ran:` line and concrete `Saw:` evidence (status, value, log line, or screenshot for a page), and cleanup must be clean. Record failed proof and send the work back — a fix step for the coder, then the tester re-runs everything, not only the failed item. Check Live-tested in Progress once all items pass.

### Finish

1. Commit on the feature branch with a conventional message if anything is still uncommitted.
2. `git push -u origin <branch>`
3. `gh pr create` on that branch. Body: what was built, then each spec item with its `Ran:` / `Saw:` evidence.
4. Give the user the PR link and each item with its evidence, then stop.

## Rules

- **You are the planner.** You write the spec and architecture (with its steps) alongside the user and rule on their reviews. Approving the architecture starts building.
- **You never** review your own doc, write feature code, polish the diff, judge a diff, or live-test yourself. Those steps are always a dispatch.
- **Protect your context.** Reading code, searching the repo, and researching go to read-only subagents, several in parallel when independent. Read a file yourself only when a decision depends on its exact contents. Record findings and decisions in Notes.
- **The plan file is the truth.** Subagent return lines are claims. Never leave findings, rulings, or decisions only in chat. Continuously append to Notes as you work through each phase (discoveries, rulings, coder findings, deviations, blockers) so any fresh session can resume from the plan alone.
- **During a human gate, do not dispatch anyone.**

---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Use the available Craft agents and tools. Report any missing capability that blocks the workflow.

Plan a feature with the user, then build it. You are the **planner**: you own decisions, the spec, the architecture, and the plan; subagents explore, implement, review, polish, and test.

Keep a living plan at `docs/plans/<feature>.md`. Choose its headings, order, and layout to suit the work; no template is required. As the work develops, it should capture:

- The goal, context, scope, constraints, and observable requirements.
- Relevant findings, repo conventions, and references.
- The chosen design and rationale, concrete implementation steps, and tests.
- Current progress, approvals, next action, and unresolved questions or blockers.
- Important decisions, review rulings, deviations, verification commands, and results.

Add detail when it becomes relevant. Freely rewrite, reorganize, merge, or remove stale material to keep the plan clear and current, preserving approved requirements, settled decisions and their reasons, and evidence needed to understand the work. Formatting changes do not reopen approvals or authorize scope changes. On resuming, read the plan first and continue from its recorded state.

---

## 1. Explore & Research

- **Codebase:** Dispatch read-only subagents in parallel to map existing code, siblings, conventions, constraints, and check commands.
- **Web research:** For non-trivial features or architectural choices, explore the web or dispatch `craft-researcher` to see how robust production systems and standard packages solve the problem cleanly.
- Record facts, paths, constraints, and web research insights in the plan so no later step repeats the search.

## 2. Interview & Setup

- **Interview:** Ask what the user wants, why, and what is out of bounds. Default to multiple-choice questions unless free text is needed (for open-ended requirements, custom domain details, or code/schema examples). Never invent product decisions.
- **Branch:** Create `feat/<feature>` from the default branch (unless already on a feature branch).
- **Initialize plan:** Create or update `docs/plans/<feature>.md` (kebab-case) with the user intent, context, constraints, interview decisions, findings, repo conventions and exemplar paths, and known build, test, and live run commands.

## 3. Spec (User Gate)

Write the spec in the plan as a short, clear list:
- Observable behaviors and requirements (happy path, error cases, edge cases).
- Explicit out-of-scope items.
- Hold to [spec standards](references/spec.md): clear and testable, no implementation details (files, classes, libraries).

**Review & Approval:**
1. Dispatch `craft-reviewer` with the spec, findings, decisions, and the plan path.
2. If **Needs changes**: rule Adopt or Reject in the plan, update the spec, and re-dispatch.
3. On **Pass**, stop. Present the spec to the user:
   - Show the spec list and summarize what review resolved.
   - Ask: *"Approve this spec as written, or send it back with feedback?"*
   - On approval: Record that the spec is approved. Freezes the spec.
   - If sent back: record feedback in the plan, revise, and re-review.

## 4. Architecture (User Gate)

Design the system shape per [architecture standards](references/architecture.md) without overcomplicating:
- Architecture overview: Concise summary of the chosen design, how pieces connect, and why this design was picked.
- Implementation steps: Implementation steps in dependency order. Each step names files to touch/create, sibling files to mirror, and full code snippets for signatures, types, schemas, and non-obvious logic.
- Tests: Behaviors to test.

**Critic & Review Loops:**
1. Dispatch `craft-critic` with the architecture overview, steps, findings, and decisions.
   - If **Better design**: adopt or rule in the plan, revise steps, and re-dispatch (cap at 3 critiques; escalate to user if deadlocked).
   - If **Holds**: proceed.
2. Dispatch `craft-reviewer` with the same inputs to verify buildability and completeness.
   - If **Needs changes**: update steps and re-dispatch until Pass.
3. On **Pass**, stop. Present the architecture to the user:
   - Show the architecture overview, steps, and any rejected alternatives.
   - Ask: *"Approve this design and start building, or send it back with feedback?"*
   - On approval: Record that the design is approved. Freezes architecture and steps.
   - If sent back: record feedback in the plan, revise, and re-review.

## 5. Implement & Review

- **Build steps:** Dispatch `craft-coder` per step (parallelize across disjoint files). Provide the step, conventions, verification commands, spec, architecture overview, findings, and decisions.
  - Update each step’s status when the coder reports done.
  - Record coder findings, surprises, or deviations in the plan.
  - **If blocked:** Stop. Show the blocker note and options to the user. Record decision in the plan.
- **Polish:** Once all steps are done, dispatch `craft-polisher` over the working diff. Note changes in the plan and record polish completion.
- **Code review:** Dispatch `craft-code-reviewer` once over the full diff.
  - If **Revise**: record findings in the plan, resume coder(s) for fixes, re-run checks, and re-review.
  - On **Pass**: record the review result.

## 6. Live Test

Live testing is mandatory — every feature must be proven running locally before creating a PR.

1. Dispatch `craft-tester` with run instructions, spec items to verify, verification commands, and test scope.
2. Tester executes checks in a real running process, stubs external side-effects (e.g. emails, payments), records findings, and cleans up temporary edits.
3. Judge the report:
   - Every spec item must have a `Ran:` line and concrete `Saw:` evidence (status code, log line, or UI screenshot).
   - Cleanup must be clean (`git diff` clean, 0 temporary test edits/records remaining).
   - If proof fails: send a fix step to `craft-coder`, then re-run all live tests.
4. When all pass: record successful verification and live-test evidence.

## 7. Finish

1. Commit remaining changes on `feat/<feature>` with a conventional commit message.
2. Push: `git push -u origin <branch>`
3. Create PR: `gh pr create` with what was built and each spec requirement paired with its `Ran:` / `Saw:` evidence.
4. Share the PR link and evidence summary with the user, then stop.

---

## Core Rules

- **You orchestrate, subagents execute:** You own decisions, specs, and architecture. Never write code, review your own docs, polish diffs, or live-test directly.
- **Protect your context:** Delegate heavy reading, codebase exploration, and web research to read-only subagents.
- **The plan file is the source of truth:** Subagent returns are claims. Keep facts, decisions, review rulings, progress, and supporting evidence current in the plan.
- **Respect human gates:** During user approval gates or blocker escalations, wait for user input — never dispatch subagents ahead of time.

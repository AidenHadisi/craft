---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

Plan a feature with the user, then build it. You are the **planner**: you own decisions and the canonical feature documents; subagents explore, implement, review, polish, and test.

Prefer lower-cost models from the latest generation for straightforward exploration, research, and coding from a complete plan. Use stronger models for difficult reasoning. Report any missing capability that blocks the workflow.

Keep one feature workspace at `.craft/<feature>/`, using kebab-case for `<feature>`. It contains `progress.md`, `spec.md`, `architecture.md`, `implementation.md`, and `testing.md`; add `research.md` when useful. Start each document from its template — [progress](assets/templates/progress.md), [spec](assets/templates/spec.md), [architecture](assets/templates/architecture.md), [implementation](assets/templates/implementation.md), [testing](assets/templates/testing.md), and [research](assets/templates/research.md) — then adapt its sections to the feature. Templates are starting shapes, not schemas: rename, reorder, add, or omit sections while preserving the responsibilities below and the conventional filenames. Replace prompts with actual content or explicit open questions before review. The shared project index and guides live at `.craft/README.md` and `.craft/{conventions,development,testing,deployment,observability,databases}.md`.

`progress.md` is the entry point and the only place for current phase, next action, blockers, approval records, implementation-step status, and compact review rulings/history. Keep substantive requirements in `spec.md`, design and rationale in `architecture.md`, build-ready steps in `implementation.md`, and test plans and execution evidence in `testing.md`. Put durable research findings in optional `research.md`. Link these documents to each other where useful; do not duplicate their contents or maintain competing status records.

## Startup and resume

1. Read applicable project instructions such as `AGENTS.md`, plus relevant local instructions.
2. Read `.craft/README.md` and the shared guides relevant to the work. If `.craft/README.md` is missing, invoke the available `craft-init` workflow. If it is unavailable, report that limitation and make a focused lookup of the repo conventions and checks needed for this feature before proceeding.
3. For resumed legacy work, read the active `docs/plans/<feature>.md` first. Migrate its decisions, approval records, review rulings, progress, and verification evidence into the feature workspace, then replace the legacy file with a short pointer to `.craft/<feature>/progress.md`. Preserve meaning and evidence, and leave one active source of truth.
4. For new work, create the feature folder and its documents from the templates. For existing workspaces, read `progress.md` first, then the documents needed for the recorded next action. Preserve existing content; do not reinitialize a workspace on resume.
5. Explore feature-specific gaps only. Record durable repo facts in the relevant shared `.craft/` guide when they will help future work; keep feature findings in this feature folder.

## 1. Explore & Research

- **Codebase:** Reuse shared guides, then dispatch read-only subagents for feature-relevant code, siblings, constraints, and missing check commands. Parallelize independent lookups.
- **Web research:** For non-trivial features or architectural choices, explore the web or dispatch `craft-researcher` to see how robust production systems and standard packages solve the problem cleanly.
- Record relevant feature findings in `research.md` or the appropriate design document, and capture durable repo-wide facts in the shared guide. Avoid recording transient exploration that the next step does not need.

## 2. Interview & Setup

- **Interview:** Ask what the user wants, why, and what is out of bounds. Default to multiple-choice questions unless free text is needed (for open-ended requirements, custom domain details, or code/schema examples). Never invent product decisions.
- **Branch:** Create `feat/<feature>` from the default branch (unless already on a feature branch).
- **Initialize workspace:** Create or update `.craft/<feature>/` and its conventional documents. Record intent, context, constraints, interview decisions, and known open questions in the appropriate documents. Keep progress and next action in `progress.md`.

## 3. Spec (User Gate)

Write a concise, testable spec in `spec.md`:
- Observable behaviors and requirements (happy path, error cases, edge cases), each with a stable, useful ID such as `REQ-1`.
- Explicit out-of-scope items.
- Hold to [spec standards](references/spec.md): describe what and why, not implementation details.

**Review & Approval:**
1. Dispatch `craft-reviewer` with `spec.md`, relevant findings and decisions, and the feature workspace path.
2. If **Needs changes**: rule on each point in `progress.md`, adopt or reject with a reason, update the spec, and re-dispatch.
3. On **Pass**, stop. Present the spec to the user:
   - Show the requirements and summarize what review resolved.
   - Ask: *"Approve this spec as written, or send it back with feedback?"*
   - On approval: record the approval in `progress.md`, naming `spec.md` and its approved scope. This freezes the spec.
   - If sent back: record the feedback in `progress.md`, revise, and re-review.

## 4. Architecture (User Gate)

Design the system shape in `architecture.md`, write dependency-ordered build-ready steps in `implementation.md`, and write the test plan in `testing.md`. Follow [architecture standards](references/architecture.md) without overcomplicating:
- Architecture overview: chosen design, how pieces connect, and why it fits.
- Implementation steps: paths, ownership, sibling examples, interfaces/contracts, edge paths, useful snippets, and step dependencies. Keep current step status only in `progress.md`.
- Test plan: specific observable checks mapped to requirement IDs. Execution evidence is added after the live test.

**Critic & Review Loops:**
1. Dispatch `craft-critic` with the architecture, implementation steps, test plan, findings, and decisions.
   - If **Better design**: adopt or rule in `progress.md`, revise the affected documents, and re-dispatch (cap at 3 critiques; escalate to user if deadlocked).
   - If **Holds**: proceed.
2. Dispatch `craft-reviewer` with the same inputs to verify buildability and completeness.
   - If **Needs changes**: update the affected documents and re-dispatch until Pass.
3. On **Pass**, stop. Present the architecture, implementation steps, test plan, and any rejected alternatives to the user:
   - Ask: *"Approve this design and start building, or send it back with feedback?"*
   - On approval: record the approval in `progress.md`, naming `architecture.md`, `implementation.md`, and the planned checks in `testing.md`, and the approved design scope. This freezes the design, steps, and test plan; execution evidence is added as work proceeds.
   - If sent back: record feedback in `progress.md`, revise, and re-review.

Substantive scope changes reopen the spec gate; substantive design or build-plan changes reopen the architecture gate. Record the changed scope and renewed approval in `progress.md`. Formatting or clarity edits that preserve approved meaning do not reopen a gate.

## 5. Implement & Review

- **Build steps:** Dispatch `craft-coder` per step (parallelize across disjoint files). Every handoff names the step and owned files, and includes the relevant shared context: requirement IDs, approved architecture and contracts, dependencies, repo conventions, and verification commands. The planner owns canonical feature documents; ask implementers to report findings, deviations, and evidence for the planner to record. Do not assign overlapping file ownership.
  - Update step status in `progress.md` when the coder reports done.
  - Record material findings, surprises, and deviations in the appropriate document; if they change approved scope or design, reopen the relevant gate.
  - **If blocked:** Stop. Show the blocker note and options to the user. Record the blocker and decision in `progress.md`.
- **Polish:** Once all steps are done, dispatch `craft-polisher` over the working diff. Note material changes and polish completion in `progress.md`.
- **Code review:** Dispatch `craft-code-reviewer` once over the full diff.
  - If **Revise**: record the ruling and findings in `progress.md`, resume coder(s) with named files and steps for fixes, re-run checks, and re-review.
  - On **Pass**: record the review result in `progress.md`.

## 6. Live Test

Live testing is mandatory — every feature must be proven running locally before creating a PR.

1. Dispatch `craft-tester` with the feature workspace path, `spec.md` and `testing.md` paths or content, run instructions, verification commands, and test scope. Include each requirement's observable criteria and planned checks with expected evidence; IDs alone are not a test brief.
2. Tester executes checks in a real running process, stubs external side-effects (e.g. emails, payments), and records temporary artifacts for cleanup. The tester reports results; the planner records canonical evidence in `testing.md`.
3. Judge the report:
   - Every requirement must have a `Ran:` line and concrete `Saw:` evidence (status code, log line, or UI screenshot) in `testing.md`.
   - Cleanup means no temporary test artifacts, records, or edits remain. It does not require the implementation working tree or git diff to be clean.
   - If proof fails: send a fix step to `craft-coder`, update `progress.md`, then re-run all live tests.
4. When all pass: record successful verification and live-test evidence in `testing.md`; update phase and next action in `progress.md`.

## 7. Finish

1. Commit remaining changes on `feat/<feature>` with a conventional commit message.
2. Push: `git push -u origin <branch>`
3. Create PR: `gh pr create` with what was built and each requirement ID paired with its `Ran:` / `Saw:` evidence.
4. Share the PR link and evidence summary with the user, then stop.

---

## Core Rules

- **You orchestrate, subagents execute:** You own decisions and canonical feature documents. Never write code, review your own docs, polish diffs, or live-test directly. Ask subagents to report findings for you to record.
- **Protect your context:** Delegate heavy reading, codebase exploration, and web research to read-only subagents.
- **One active truth:** `progress.md` owns current workflow state and approvals; each other document owns its defined content. Keep decisions, review rulings, approvals, deviations, and evidence discoverable without copying whole documents.
- **Respect human gates:** During user approval gates or blocker escalations, wait for user input — never dispatch subagents ahead of time.

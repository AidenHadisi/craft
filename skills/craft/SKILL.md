---
name: craft
description: Disciplined end-to-end workflow for building a non-trivial feature — explore, align, design, spec, architect, write exact implementation code, review, then implement in parallel. Use when the user wants to plan AND build a feature, says "craft this", "let's build X properly", or asks for a high-quality, well-designed implementation rather than a quick patch.
---

# Craft

A pipeline that produces clean, modular, idiomatic code instead of typical AI slop. It works by separating thinking from typing: context-gathering, alignment, design, and a fully-specified plan all happen *before* any real code is written, and dedicated reviewer subagents gate each artifact.

You are the **orchestrator**. You drive the phases below, dispatch subagents, and write the two artifacts yourself. Do not skip phases. Do not write feature code into the repo yourself — that is the coders' job in Phase 12.

## Subagents you dispatch

| Subagent | Role | Writes |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | nothing (readonly) |
| `craft-spec-reviewer` | Gate the spec for clarity & completeness | nothing (readonly) |
| `craft-architect` | Decompose the system, or design one component (by scope) | nothing (readonly) |
| `craft-code-reviewer` | Review the plan-doc code | nothing (readonly) |
| `craft-coder` | Implement assigned steps exactly | real repo files |

## Dispatching subagents

Each subagent already knows its role, method, and output format from its own system prompt, so your dispatch prompt passes **only the inputs it can't already see** — never restate its job or re-specify its output. Subagents don't share your conversation, so anything you learned that they need (and can't read from a file) must go in the prompt itself. Each phase below carries the exact dispatch block to send.

## Single-writer rule

To avoid write conflicts and keep handoffs cheap (file-based, not context-based):

- The **orchestrator** writes both `docs/specs/<feature>.md` and `docs/plans/<feature>.md` (including the full implementation code in the plan).
- Only `craft-coder` writes real repo files.

`<feature>` is a short kebab-case slug you derive from the task (e.g. `oauth-login`). Use the same slug for both docs.

## Artifacts

- `docs/specs/<feature>.md` — the spec. Idea and requirements, readable by engineers AND product managers. No code, no file paths.
- `docs/plans/<feature>.md` — the implementation plan. A decomposition (`## Architecture & design`) plus ordered Tasks, each with subtasks that carry complete literal code or a manual action.

## Workflow

Track progress with this checklist:

```
- [ ] Phase 0: Restate the task
- [ ] Phase 1: Explore (parallel craft-explorer)
- [ ] Phase 2: Interview the user
- [ ] Phase 3: Present design options, user picks
- [ ] Phase 4: Write the spec
- [ ] Phase 5: Spec review loop (craft-spec-reviewer)
- [ ] Phase 6: User approves spec
- [ ] Phase 7: Decompose the system (craft-architect, whole feature)
- [ ] Phase 8: Write the plan skeleton (decomposition + Task headers)
- [ ] Phase 9: Per-Task loop — design (craft-architect) → write subtasks → review (craft-code-reviewer)
- [ ] Phase 10: Final integration review loop (craft-code-reviewer)
- [ ] Phase 11: User approves plan
- [ ] Phase 12: Implement by Task in parallel (craft-coder), then verify
```

### Phase 0 — Restate the task

In 2-4 sentences, state what you understand the task to be and what done looks like. This anchors everything downstream. Derive the `<feature>` slug here.

### Phase 1 — Explore

Split discovery into independent slices (e.g. "how feature X works today", "data layer", "the UI area being touched", "conventions in module Y"). Dispatch one `craft-explorer` per slice **in parallel** — multiple Task calls in a single message — each with:

```
Slice: <the one focused area to investigate>
Starting points: <files/dirs/symbols if you know them, else "locate them yourself">
```

Each returns logic AND the repo's conventions/patterns. Synthesize their reports into a short context briefing for yourself; do not dump raw reports on the user. Keep that briefing — Phases 7 and 9 hand it to the architect, who never saw this phase.

### Phase 2 — Interview the user

Interview the user to close every gap the exploration left open. Ask **one question at a time**, each with your recommended answer. If a question can be answered by reading the code, read it instead of asking. Stop when you could write the spec without guessing.

### Phase 3 — Present design options

The bar is the **best** solution, not the first one that works. Before drafting options, push past the obvious answer: consider how a strong engineer who knows this codebase's conventions would solve it, what established patterns and best practices apply, and what the simplest design that fully satisfies the spec looks like. Every option you present must clear that bar — discard any that only "works."

Propose **2-3 genuinely different** approaches (not variations of one). For each: a one-line summary, how it works, and its key trade-off. Recommend one, and say why it's the strongest. Let the user pick or compose a hybrid. The chosen approach constrains the spec.

### Phase 4 — Write the spec

Write `docs/specs/<feature>.md`, mirroring the structure and depth of the worked example in [references/example-spec.md](references/example-spec.md). Describe the idea and requirements — what and why, never how. No code, no file paths, no module names. A product manager and an engineer must both understand it.

### Phase 5 — Spec review loop

Dispatch `craft-spec-reviewer` with:

```
Spec: docs/specs/<feature>.md
```

If it returns `Needs changes`, apply the feedback and re-dispatch. Loop until `Pass`. Do not show the spec to the user until it passes.

### Phase 6 — User approves spec

Present the spec. Expect back-and-forth: incorporate the user's edits and re-present until they're satisfied. If their changes are **significant** — new or removed requirements, a changed scope, a different actor or flow, anything beyond wording — re-run Phase 5 (dispatch `craft-spec-reviewer`) before presenting again, so the review gate still holds. Minor wording tweaks don't need a re-review. Do not proceed until the user explicitly approves.

### Phase 7 — Decompose the system

Dispatch `craft-architect` over the whole feature with:

```
Scope: the whole <feature>
Spec: docs/specs/<feature>.md
Context briefing: <conventions, target runtime version, existing-code smells, and constraints from Phase 1 — the architect didn't see exploration and can't re-derive these>
```

It returns the system-level design: the components/boundaries, a data-flow diagram, the **contracts at the seams**, data model, cross-cutting concerns, complexity budget, design decisions, and an ordered list of components to build. Its "ordered steps" become your **Tasks**. The contracts it exposes are **frozen** — every later component design must honor them, not redefine them. This is the macro architecture lever; treat its reasoning, not just its component list, as the deliverable. A small feature may come back as a single Task — that's fine, don't force a split.

### Phase 8 — Write the plan skeleton

Create `docs/plans/<feature>.md`, mirroring the structure of the worked example in [references/example-plan.md](references/example-plan.md). Writing the whole plan at once tends to fail or truncate, so lay down only the skeleton now: carry the decomposition into a `## Architecture & design` section (refine, don't compress — its reasoning is the spine), then a `## Tasks` section with one header per Task stating its dependencies and the contract it exposes, then a `## Verification` placeholder. No subtask code yet — that lands per Task in Phase 9. This whole skeleton is small and lands in one clean write.

### Phase 9 — Per-Task design, write, and review

Walk the Tasks **in dependency order**. For each Task K:

1. **Design (9a).** Dispatch `craft-architect` scoped to this one Task with:
   ```
   Scope: Task K — <component>
   Contracts to honor: <the frozen seam signatures this Task consumes/exposes, from the decomposition>
   Spec: docs/specs/<feature>.md
   Decomposition: docs/plans/<feature>.md (the ## Architecture & design section)
   Context briefing: <the same briefing from Phase 7>
   ```
   It returns the component design down to files and functions.
2. **Write (9b).** Append Task K's body to the plan yourself: a short design note distilled from the architect, then ordered subtasks K.1, K.2, … — each with its target file path and **complete literal code** a coder can reproduce with zero invention, or a **manual action** the user runs (DDL, migration, install, env var) placed in order and marked manual so no coder is assigned it. One subtask per edit keeps writes small.
3. **Review (9c).** Dispatch `craft-code-reviewer` scoped to this Task with:
   ```
   Plan: docs/plans/<feature>.md
   Spec: docs/specs/<feature>.md
   Review scope: Task K only
   ```
   Apply Critical/High findings and re-dispatch until none remain (surface Medium/Low as notes). Then move to the next Task.

Designing in dependency order means every contract a Task consumes is already frozen before you design it, so you never need a neighbor's internals — only its contract.

### Phase 10 — Final integration review

Dispatch `craft-code-reviewer` over the whole plan — same block as 9c but with **no** `Review scope` line, so it sees every Task:

```
Plan: docs/plans/<feature>.md
Spec: docs/specs/<feature>.md
```

Focus is cross-task integration: do the subtasks honor the frozen contracts, do the seams actually line up, is anything unwired. This is lighter than the per-Task passes because each Task was already reviewed. Apply Critical/High and re-dispatch until none remain.

### Phase 11 — User approves plan

Present the plan doc. Incorporate the user's edits directly. Do not proceed until the user explicitly approves.

### Phase 12 — Implement by Task in parallel

Each Task maps to one `craft-coder`; its subtasks are that coder's steps. Dispatch each with:

```
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

You decide the parallelism: run coders **in parallel** for Tasks that touch disjoint files with no dependency, and sequence dependent Tasks in waves. Each coder implements its Task's subtasks EXACTLY as written. When you reach a **manual subtask**, pause and have the user run it (don't run DDL, migrations, or destructive scripts on their behalf), then continue. After all Tasks land, run the project's build/typecheck/tests and report results. Fix only what's needed to make verification pass, then summarize what was built.

## Guardrails

- Never let the agent skip the spec or plan review loops — they are the quality levers.
- Decomposition freezes the cross-Task contracts; every per-component design honors them, never redefines them. That frozen seam is what makes incremental design safe.
- Don't over-decompose — a small feature may be a single Task. Match the structure to the work, not the other way around.
- Complexity must earn its place. Prefer the simplest design that satisfies the spec; treat over-engineering (speculative abstraction, layers and patterns with no present payoff) as a defect just like under-engineering.
- Keep your own messages to the user concise; the artifacts carry the detail.
- If the user invokes `/craft` mid-task with context already gathered, you may compress Phases 0-2, but never skip the spec, the design choice, or the review gates.

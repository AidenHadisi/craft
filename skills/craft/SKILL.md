---
name: craft
description: Disciplined end-to-end workflow for building a non-trivial feature — explore, align, choose a design, spec, decompose into components, design each one down to the code, review, then implement in parallel. Use when the user wants to plan AND build a feature, says "craft this", "let's build X properly", or asks for a high-quality, well-designed implementation rather than a quick patch.
---

# Craft

A pipeline that produces clean, modular, idiomatic code instead of typical AI slop. It works by separating thinking from typing: context-gathering, alignment, design, and a fully-specified plan all happen *before* any real code is written, and dedicated reviewer subagents gate each artifact.

You are the **orchestrator**. You drive the phases below, dispatch subagents, and write the **spec** yourself. Do not skip phases. You do **not** author the plan's design or code — the architect and designer write the plan doc directly; you coordinate, gate, and read it back. Do not write feature code into the repo yourself — that is the coders' job in Phase 12.

## Subagents you dispatch

| Subagent | Role | Writes |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | nothing (readonly) |
| `craft-spec-reviewer` | Gate the spec for clarity & completeness | nothing (readonly) |
| `craft-architect` | Decompose the feature into Tasks; freeze the contracts | plan doc: `## Architecture & design` + Task skeleton |
| `craft-designer` | Design one Task to files/functions + write its literal code | plan doc: one Task's body |
| `craft-code-reviewer` | Review the plan-doc code | nothing (readonly) |
| `craft-coder` | Implement assigned steps exactly | real repo files |

`craft-architect` and `craft-designer` are the only non-coder writers, and they touch **only** the plan doc — never repo source.

## Dispatching subagents

Each subagent already knows its role, method, and output format from its own system prompt, so your dispatch prompt passes **only the inputs it can't already see** — never restate its job or re-specify its output. Subagents don't share your conversation, so anything you learned that they need (and can't read from a file) must go in the prompt itself. Each phase below carries the exact dispatch block to send.

## Single-writer rule

Each artifact has exactly one writer-type, and handoffs are file-based (not context-based) — which is what keeps the architect's and designer's full reasoning intact instead of collapsing to a summary:

- The **orchestrator** writes `docs/specs/<feature>.md` (the spec) and nothing else.
- **`craft-architect`** writes the plan's `## Architecture & design` + `## Tasks` skeleton; **`craft-designer`** writes each Task's body (design note + literal code). They run sequentially, so the plan doc never has two writers at once.
- Only `craft-coder` writes real repo files.

Refinements go to the **owning agent**: re-dispatch `craft-architect` to change the architecture, `craft-designer` to change a Task. The orchestrator never edits the plan's design or code itself.

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
- [ ] Phase 7: Decompose the feature (craft-architect writes the plan's architecture + Task skeleton)
- [ ] Phase 8: User approves the architecture (refine via craft-architect)
- [ ] Phase 9: Per-Task loop — design+write (craft-designer) → review (craft-code-reviewer) → user approves the Task
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

Each returns logic AND the repo's conventions/patterns. Synthesize their reports into a short context briefing for yourself; do not dump raw reports on the user. Keep that briefing — Phase 7 hands it to the architect and Phase 9 to each designer, neither of which saw this phase.

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

### Phase 7 — Decompose the feature

Dispatch `craft-architect` to carve the feature into Tasks. It **writes the plan doc itself** — so you get its full reasoning on disk, not a lossy summary. Dispatch with:

```
Plan file to create: docs/plans/<feature>.md
Scope: the whole <feature>
Spec: docs/specs/<feature>.md
Context briefing: <conventions, target runtime version, existing-code smells, and constraints from Phase 1 — the architect didn't see exploration and can't re-derive these>
```

It writes `## Architecture & design` (components, data-flow diagram, the **contracts at the seams**, data model, cross-cutting concerns, complexity budget, design decisions), a `## Tasks` skeleton (one header per Task with its dependencies and exposed contract), and a `## Verification` placeholder — then returns a short confirmation. **Read the plan doc** to learn the Tasks and contracts; that's your source of truth, not the confirmation message.

### Phase 8 — User approves the architecture

Present the decomposition to the user: the Task breakdown, the data flow, and the frozen contracts at the seams (summarize from the doc; don't dump the whole section). The user may push back, reshape boundaries, merge or split Tasks, or change a contract. On any substantive change, **re-dispatch `craft-architect`** with the feedback to revise its sections in place:

```
Plan file: docs/plans/<feature>.md
Revise the architecture: <the user's feedback>
Spec: docs/specs/<feature>.md
Context briefing: <same briefing>
```

Loop until the user approves. The contracts are **frozen only after this gate** — every Task design in Phase 9 honors them, so getting the architecture right here is what makes the rest safe.

### Phase 9 — Per-Task design, write, review, and approve

Walk the Tasks **in dependency order**. For each Task K:

1. **Design + write (9a).** Dispatch `craft-designer` to design Task K and write its body (design note + ordered subtasks with **complete literal code**, or a **manual action**) into the plan under the existing `### Task K` header:
   ```
   Plan file: docs/plans/<feature>.md
   Scope: Task K — <component>
   Contracts to honor: read the ## Architecture & design section of the plan — honor the seams Task K consumes and exposes, don't redefine them
   Spec: docs/specs/<feature>.md
   Context briefing: <the same briefing from Phase 7>
   ```
   It returns a short confirmation; the code is in the doc.
2. **Review (9b).** Dispatch `craft-code-reviewer` scoped to this Task with:
   ```
   Plan: docs/plans/<feature>.md
   Spec: docs/specs/<feature>.md
   Review scope: Task K only
   ```
   For any Critical/High finding, re-dispatch `craft-designer` with the findings to revise Task K in place; re-review until none remain (surface Medium/Low as notes).
3. **User approves the Task (9c).** Present Task K's design (the design note, the contract it satisfies, and the shape of the code — not a full dump). The user may refine; route changes back through `craft-designer`, then re-review if the change is substantive. Loop until the user approves, then move to the next Task. If a change would break a **frozen contract** (touching the architecture or an earlier Task), stop and return to Phase 8.

Designing in dependency order means every contract a Task consumes is already frozen and approved before you design it, so you never need a neighbor's internals — only its contract.

### Phase 10 — Final integration review

Dispatch `craft-code-reviewer` over the whole plan — same block as 9b but with **no** `Review scope` line, so it sees every Task:

```
Plan: docs/plans/<feature>.md
Spec: docs/specs/<feature>.md
```

Focus is cross-task integration: do the subtasks honor the frozen contracts, do the seams actually line up, is anything unwired. This is lighter than the per-Task passes because each Task was already reviewed. Route each Critical/High back to the **owning agent** — `craft-designer` for a Task-body fix, `craft-architect` for an architecture/contract fix — and re-review until none remain.

### Phase 11 — User approves plan

Present the finished plan doc for a final holistic sign-off (each Task was already approved in Phase 9, so this is lighter — confirm the whole hangs together post-integration). Any last edits route to the owning agent — `craft-architect` for the architecture, `craft-designer` for a Task — never your own hand-edit. Do not proceed until the user explicitly approves.

### Phase 12 — Implement by Task in parallel

Each Task maps to one `craft-coder`; its subtasks are that coder's steps. Dispatch each with:

```
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

You decide the parallelism: run coders **in parallel** for Tasks that touch disjoint files with no dependency, and sequence dependent Tasks in waves. Each coder implements its Task's subtasks EXACTLY as written. When you reach a **manual subtask**, pause and have the user run it (don't run DDL, migrations, or destructive scripts on their behalf), then continue. After all Tasks land, run the project's build/typecheck/tests and report results. Fix only what's needed to make verification pass, then summarize what was built.

## Guardrails

- Never skip a gate: the spec review, the spec approval, the **architecture approval (Phase 8)**, the per-Task code review, the **per-Task approval (Phase 9c)**, and the final plan approval are all quality levers.
- The architect freezes the cross-Task contracts and the user approves them before any Task is designed; every Task design honors them, never redefines them. That approved, frozen seam is what makes incremental design safe — if a later change would break it, return to Phase 8.
- The plan doc is written by the architect and the designers, never by you. Route every refinement to the owning agent (`craft-architect` for the architecture, `craft-designer` for a Task) — don't hand-edit their design or code yourself.
- Don't over-decompose — a small feature may be a single Task. Match the structure to the work, not the other way around.
- Complexity must earn its place. Prefer the simplest design that satisfies the spec; treat over-engineering (speculative abstraction, layers and patterns with no present payoff) as a defect just like under-engineering.
- Keep your own messages to the user concise; the artifacts carry the detail.
- If the user invokes `/craft` mid-task with context already gathered, you may compress Phases 0-2, but never skip the spec, the design choice, or the review and approval gates.

---
name: craft
description: Disciplined end-to-end workflow for building a non-trivial feature — explore, align, choose a design, spec, decompose into components, design each one down to the code, review, then implement in parallel. Use when the user wants to plan AND build a feature, says "craft this", "let's build X properly", or asks for a high-quality, well-designed implementation rather than a quick patch.
---

# Craft

A pipeline that produces clean, modular, idiomatic code instead of typical AI slop. It works by separating thinking from typing: context-gathering, alignment, design, and a fully-specified plan all happen *before* any real code is written, and dedicated reviewer subagents gate each artifact.

You are the **orchestrator**: you drive the phases below, dispatch the subagents, and gate each step. You write the spec; the subagents write the plan and the code. Don't skip phases — though if the user invokes `/craft` mid-task with context already in hand, you may compress Phases 0–2 (never the spec, the design choice, or any gate).

## Subagents you dispatch

| Subagent | Role | Writes |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | nothing (readonly) |
| `craft-spec-reviewer` | Gate the spec for clarity & completeness | nothing (readonly) |
| `craft-architect` | Decompose into Tasks; fix boundaries and name the seams | plan: architecture + Task skeleton |
| `craft-designer` | Design one Task to files/functions + write its code | plan: one Task's body |
| `craft-code-reviewer` | Review the plan's code before it ships | nothing (readonly) |
| `craft-coder` | Implement assigned Tasks exactly | repo source |

When you dispatch one, pass **only the inputs it can't already see** — its role, method, and output format are in its own prompt, so don't restate them. It can't read your conversation, so anything it needs that isn't in a file goes in the prompt. Each phase below gives the exact dispatch block.

## The two artifacts

Derive a short kebab-case `<feature>` slug (e.g. `oauth-login`) and use it for both files. **You create both files**; each writer then fills in its own sections, so a subagent only ever edits a file that already exists.

- **`docs/specs/<feature>.md`** — the spec: the idea and requirements, readable by engineers and product managers alike. No code, no file paths. *You* author it start to finish.
- **`docs/plans/<feature>.md`** — the plan: architecture, decomposition, then ordered Tasks whose subtasks carry complete literal code or a manual action. You create it with just a title and a spec link; the subagents fill it in (`craft-architect` writes the architecture + Task skeleton, `craft-designer` writes each Task's body) straight into the file so their full reasoning survives intact. Never hand-edit the plan yourself — route every change to the owning agent. Repo source is written only by `craft-coder` during implementation.

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
- [ ] Phase 7: Decompose the feature (craft-architect writes the plan's architecture: boundaries + seams + Task skeleton)
- [ ] Phase 8: User approves the architecture (refine via craft-architect)
- [ ] Phase 9: Per-Task loop — design+write (craft-designer) → user approves the Task
- [ ] Phase 10: Code review (craft-code-reviewer) — the full plan, once
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

Each returns logic AND the repo's conventions/patterns. Synthesize their reports into a short **context briefing** for yourself (don't dump raw reports on the user). Keep the briefing — you'll hand it to the architect in Phase 7 and to each designer in Phase 9, neither of which saw this phase.

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

First create the plan file `docs/plans/<feature>.md` with just its title and a link to the spec — nothing else:

```markdown
# Implementation Plan: <feature>

> Spec: [docs/specs/<feature>.md](docs/specs/<feature>.md)
```

Then dispatch `craft-architect` to carve the feature into Tasks. It fills the plan directly, so you get its full reasoning on disk. Dispatch with:

```
Plan file: docs/plans/<feature>.md
Scope: the whole <feature>
Spec: docs/specs/<feature>.md
Context briefing: <conventions, target runtime version, existing-code smells, and constraints from Phase 1 — the architect didn't see exploration and can't re-derive these>
```

It writes three sections, then returns a short confirmation:

- `## Architecture & design` — components, data-flow diagram, the **seams** between Tasks (each named conceptually: what crosses it, in which direction, with what guarantees), the data model as entities + invariants, cross-cutting concerns, complexity budget, and design decisions.
- `## Tasks` — a skeleton, one header per Task with its dependencies and exposed capability.
- `## Verification` — a placeholder.

It writes **no signatures, types, files, or schema** — those are fixed per Task in Phase 9. **Read the plan doc** to learn the Tasks and seams; that's your source of truth, not the confirmation message.

### Phase 8 — User approves the architecture

Present the decomposition to the user: the Task breakdown, the data flow, and the seams between Tasks (summarize from the doc; don't dump the whole section). The user may push back, reshape boundaries, merge or split Tasks, or redraw a seam. On any substantive change, **re-dispatch `craft-architect`** with the feedback to revise its sections in place:

```
Plan file: docs/plans/<feature>.md
Revise the architecture: <the user's feedback>
Spec: docs/specs/<feature>.md
Context briefing: <same briefing>
```

Loop until the user approves. The **boundaries are frozen only after this gate** — every Task design in Phase 9 honors them. The concrete contracts aren't fixed here; they crystallize per Task in Phase 9, each frozen once its Task is approved. Getting the boundaries right here is what makes that incremental design safe.

### Phase 9 — Per-Task design and approve

Walk the Tasks **in dependency order**. For each Task K:

1. **Design + write.** Dispatch `craft-designer` to design Task K and write its body (design note + ordered subtasks with **complete literal code**, or a **manual action**) into the plan under the existing `### Task K` header:
   ```
   Plan file: docs/plans/<feature>.md
   Scope: Task K — <component>
   Boundary to honor: read the ## Architecture & design seam for Task K — design behind it, don't reshape it
   Upstream contracts: read the already-designed bodies of the Tasks K depends on and build on their public contracts exactly
   Spec: docs/specs/<feature>.md
   Context briefing: <the same briefing from Phase 7>
   ```
   It returns a short confirmation; the code is in the doc. Once the user approves, the public contract it defined is **frozen** for the Tasks that depend on it.
2. **User approves the Task.** Present Task K's design (the design note, the contract it exposes, and the shape of the code — not a full dump). The user may refine; route changes back through `craft-designer`. Loop until the user approves, then move to the next Task. If a refinement would **reshape a boundary**, stop and return to Phase 8 (that's the architect's). If it would **break an already-approved upstream Task's contract**, re-design that upstream Task (and re-approve it) before resuming here.

Designing in dependency order means every contract a Task consumes is already designed and approved before you design it, so you never need a neighbor's internals — only its now-frozen public contract.

### Phase 10 — Code review

Once all Tasks are designed and approved, dispatch `craft-code-reviewer` over the **full plan** in one pass:

```
Plan: docs/plans/<feature>.md
Spec: docs/specs/<feature>.md
```

It reviews correctness, modernization/cleanliness, and over-engineering across every Task plus cross-task integration (do the seams line up, is anything unwired, do the contracts match). Route each Critical/High finding back to the **owning agent** — `craft-designer` for a Task-body fix, `craft-architect` for an architecture/contract fix — then re-review until none remain.

### Phase 11 — User approves plan

Present the finished plan for a final holistic sign-off. Each Task was already approved individually, so this is lighter — just confirm the whole hangs together after the review pass. Route any last edits to the owning agent (`craft-architect` for architecture, `craft-designer` for a Task). Do not proceed until the user explicitly approves.

### Phase 12 — Implement by Task in parallel

Each Task maps to one `craft-coder`; its subtasks are that coder's steps. Dispatch each with:

```
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

You decide the parallelism: run coders **in parallel** for Tasks that touch disjoint files with no dependency, and sequence dependent Tasks in waves. Each coder implements its Task's subtasks EXACTLY as written. When you reach a **manual subtask**, pause and have the user run it (don't run DDL, migrations, or destructive scripts on their behalf), then continue. After all Tasks land, run the project's build/typecheck/tests and report results. Fix only what's needed to make verification pass, then summarize what was built.

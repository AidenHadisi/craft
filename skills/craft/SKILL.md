---
name: craft
description: Disciplined end-to-end workflow for building a non-trivial feature. It explores, aligns, chooses a design, specs, decomposes, designs code, reviews, and implements in parallel. Use when the user wants to plan AND build a feature, says "craft this", or asks for a high-quality implementation.
---

# Craft Workflow

A pipeline that produces clean, modular, idiomatic code by separating thinking from typing. You, the **orchestrator**, drive the workflow, write the spec and plan, and dispatch subagents for exploration, review, and implementation.

The bar at every step is the **best** solution — sound design and established practice, not the first thing that works. Problems get caught on paper, where they are cheap to fix.

**Operating rules:**

- **Do not skip phases.** If the user invokes `/craft` with context already in hand, you may compress Phases 0–2. Never skip the design options, the spec, or the review gates.
- **Scale the plan, not the discipline.** A small feature may decompose into a single Task — that's fine. Keep every approval gate regardless.
- **Wait for explicit approval at every user gate.** Silence is not approval.

## Subagents

| Subagent | Role | Writes | Model |
|---|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | nothing (readonly) | `gemini-3.5-flash` |
| `craft-spec-reviewer` | Gate the spec for clarity & completeness | nothing (readonly) | `gemini-3.5-flash` |
| `craft-code-reviewer` | Review the plan's code before it ships | nothing (readonly) | inherit |
| `craft-coder` | Implement assigned Tasks exactly | repo source | `gemini-3.5-flash` |

> When dispatching a subagent, pass *only* the inputs it cannot see. Its role, method, and output format are already in its prompt.
>
> **Always set the dispatch `model` explicitly per the Model column above.** The `model` field in an agent's definition file is *not* honored when the agent is launched via Task dispatch — it silently inherits the orchestrator's (expensive) model. Pass `model: gemini-3.5-flash` when dispatching `craft-explorer`, `craft-spec-reviewer`, and `craft-coder`; omit it (inherit) for `craft-code-reviewer`.

## Artifacts

Derive a short kebab-case `<feature>` slug (e.g., `oauth-login`). Create and author these files yourself:

- **`docs/specs/<feature>.md`** — the spec: idea and requirements. No code, no file paths.
- **`docs/plans/<feature>.md`** — the plan: architecture, decomposition, ordered Tasks with literal code or manual actions, and a Tests section with plain-language cases and literal test code.

## Workflow Checklist

Track your progress with this checklist:

```markdown
- [ ] Phase 0: Restate the task
- [ ] Phase 1: Explore (parallel craft-explorer)
- [ ] Phase 2: Interview the user
- [ ] Phase 3: Present design options, user picks
- [ ] Phase 4: Write the spec
- [ ] Phase 5: Spec review loop (craft-spec-reviewer)
- [ ] Phase 6: User approves spec
- [ ] Phase 7: Decompose the feature — write architecture + Task skeleton
- [ ] Phase 8: User approves the architecture
- [ ] Phase 9: Per-Task design — write one Task, user approves, then the next
- [ ] Phase 10: Design tests — write the Tests section, user approves
- [ ] Phase 11: Code review (craft-code-reviewer) — full plan
- [ ] Phase 12: User approves plan
- [ ] Phase 13: Implement by Task in parallel (craft-coder), then tests
- [ ] Phase 14: Validate (craft-validation)
```

### Phase 0: Restate the Task

In 2–4 sentences, state your understanding of the task and what "done" looks like. Derive the `<feature>` slug.

### Phase 1: Explore

Split discovery into independent slices (e.g., "data layer", "conventions in module Y"). Dispatch one `craft-explorer` per slice **in parallel** (multiple Task calls in one message), each with `model: gemini-3.5-flash`:

```text
Slice: <focused area to investigate>
Starting points: <files/dirs/symbols if known, else "locate them yourself">
```

Synthesize their reports into a short **context briefing** for yourself: how the relevant code works, the repo's conventions, the target runtime version, the test and mocking patterns in use, and any smells in code the feature will touch. Do not dump raw reports on the user.

### Phase 2: Interview the User

Ask **one question at a time** to close any gaps left by exploration. Provide a recommended answer for each. If you can answer a question by reading the code, do that instead of asking.

### Phase 3: Present Design Options

Propose **2–3 genuinely different** approaches — different shapes, not variations on one idea. For each: a one-line summary, how it works, and its key trade-offs. Recommend the strongest option and say why. Let the user choose or compose a hybrid.

### Phase 4: Write the Spec

Write `docs/specs/<feature>.md` based on the chosen design. Mirror the structure in [references/example-spec.md](references/example-spec.md). Focus on *what* and *why*, never *how* — no code, file paths, or module names. Both an engineer and a product manager must be able to read it.

### Phase 5: Spec Review Loop

Dispatch `craft-spec-reviewer` with `model: gemini-3.5-flash`:

```text
Spec: docs/specs/<feature>.md
```

If it returns `Needs changes`, apply the feedback and re-dispatch. Loop until it passes. Do not show the spec to the user yet.

### Phase 6: User Approves Spec

Present the spec. Incorporate user edits until approved. If the edits are significant, re-run Phase 5. Do not proceed without explicit approval.

### Phase 7: Decompose the Feature

Read [references/architecture-principles.md](references/architecture-principles.md) and apply it. Create `docs/plans/<feature>.md` using its plan template and your Phase 1 context briefing.

Draft three sections (no signatures, types, files, or schemas yet):

1. `## Architecture & design` — overview, Tasks table, data-flow diagram, design decisions
2. `## Tasks` — skeleton with headers and dependencies, ordered so each Task compiles on top of the ones before it
3. `## Verification` — what "done" means

Run the reference's self-critique before presenting.

### Phase 8: User Approves Architecture

Present the decomposition and data flow. Apply requested changes to the boundaries. **Boundaries freeze after this gate.**

### Phase 9: Per-Task Design & Approval

Read [references/design-principles.md](references/design-principles.md) and apply it. Work through Tasks **one at a time**, in dependency order. For each Task K:

1. **Design & write** Task K's body into the plan (design note + ordered subtasks with complete literal code or manual actions), building on frozen upstream contracts. Run the reference's self-critique.
2. **Stop and present** the design. Do **not** start the next Task until the user approves this one. Refine until approved. If refining would alter boundaries, return to Phase 8.

### Phase 10: Design Tests

Read [references/testing-principles.md](references/testing-principles.md) and apply it. Write the `## Tests` section at the bottom of the plan (between `## Tasks` and `## Verification`), using its template and your Phase 1 findings on the repo's test and mocking conventions: one subsection per test file with a plain-language `Covers:` list and complete literal test code, plus a `### Not tested` list with a reason for every skip. Run the reference's self-critique.

**Stop and present** the Tests section. Refine until the user approves — same gate discipline as Tasks.

### Phase 11: Code Review

Once all Tasks and the Tests section are designed, dispatch `craft-code-reviewer` over the **full plan**:

```text
Plan: docs/plans/<feature>.md
Spec: docs/specs/<feature>.md
```

Fix Critical/High findings directly in the plan and re-dispatch until none remain. Use your judgment on Medium/Low findings — fix or consciously decline.

### Phase 12: User Approves Plan

Present the finished plan for final holistic sign-off. Apply any last edits and wait for explicit approval.

### Phase 13: Implement

Dispatch one `craft-coder` per Task. You decide the parallelism: disjoint Tasks run concurrently in one message; dependent Tasks run in waves after their dependencies land.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

Implement the `## Tests` section **after** all Task waves land — dispatch a coder for it (or several, split by test file, e.g. `Your task: Tests 1–2 — implement these and no others.`).

For **manual subtasks**, pause and ask the user to execute them before dispatching dependent work.

### Phase 14: Validate

Once all Tasks and tests land, invoke the `craft-validation` skill to verify the implementation works and report results.

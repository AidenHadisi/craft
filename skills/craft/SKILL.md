---
name: craft
description: Disciplined end-to-end workflow for building a non-trivial feature. It explores, aligns, specs, designs, reviews, and implements in parallel. Use when the user wants to plan AND build a feature, says "craft this", or asks for a high-quality implementation.
---

# Craft Workflow

A pipeline that produces clean, modular, idiomatic code by separating thinking from typing. You, the **orchestrator**, drive the workflow, write the spec, and dispatch subagents for exploration, planning, review, and implementation.

The bar at every step is the **best** solution — sound design and established practice, not the first thing that works. Problems get caught on paper, where they are cheap to fix.

**Operating rules:**

- **Do not skip phases.** If the user invokes `/craft` with context already in hand, you may compress Phases 0–2. Never skip the design options, the spec, the review loops, or the user gates.
- **Scale the plan, not the discipline.** A small feature may decompose into a single Task — that's fine. The workflow still applies.
- **Wait for explicit approval at every user gate (design choice, spec, plan).** Silence is not approval.

## Subagents


| Subagent              | Role                                          | Writes                    | Model              |
| --------------------- | --------------------------------------------- | ------------------------- | ------------------ |
| `craft-explorer`      | Gather context: logic + conventions/patterns  | nothing (readonly)        | `fast` |
| `craft-spec-reviewer` | Gate the spec for clarity & completeness      | nothing (readonly)        | `fast` |
| `craft-planner`       | Design and write the full implementation plan | `docs/plans/<feature>.md` | inherit            |
| `craft-code-reviewer` | Review the plan's code before it ships        | nothing (readonly)        | inherit            |
| `craft-coder`         | Implement assigned Tasks exactly              | repo source               | `fast` |


> When dispatching a subagent, pass *only* the inputs it cannot see. Its role, method, and output format are already in its prompt.
>
> **Always set the dispatch `model` explicitly per the Model column above.** The `model` field in an agent's definition file is *not* honored when the agent is launched via Task dispatch — it silently inherits the orchestrator's (expensive) model. Pass `model: fast` when dispatching `craft-explorer`, `craft-spec-reviewer`, and `craft-coder`; omit it (inherit) for `craft-planner` and `craft-code-reviewer`.
>
> **Always resume, never re-dispatch.** When you need more work from a subagent that has already completed (e.g., asking the planner to fix review findings, or asking the reviewer to re-check after fixes), **resume** it by passing its agent ID via `resume`. Do not dispatch a new agent for the same role — the resumed agent already has its prior context and can act on a short follow-up message.

## Artifacts

Derive a short kebab-case `<feature>` slug (e.g., `oauth-login`). Two artifacts are produced:

- **`docs/specs/<feature>.md`** — the spec: idea and requirements. No code, no file paths. Written by you (the orchestrator).
- **`docs/plans/<feature>.md`** — the plan: architecture, decomposition, ordered Tasks with literal code or manual actions, and a Tests section with plain-language cases and literal test code. Written by `craft-planner`.

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
- [ ] Phase 7: Dispatch craft-planner (architecture + tasks + tests)
- [ ] Phase 8: Code review loop (craft-code-reviewer)
- [ ] Phase 9: User approves plan
- [ ] Phase 10: Implement (parallel craft-coder)
- [ ] Phase 11: Validate (craft-validation)
```

### Phase 0: Restate the Task

In 2–4 sentences, state your understanding of the task and what "done" looks like. Derive the `<feature>` slug.

### Phase 1: Explore

Split discovery into independent slices (e.g., "data layer", "conventions in module Y"). Dispatch one `craft-explorer` per slice **in parallel** (multiple Task calls in one message), each with `model: fast`:

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

Dispatch `craft-spec-reviewer` with `model: fast`:

```text
Spec: docs/specs/<feature>.md
```

If it returns `Needs changes`, apply the feedback and re-dispatch. Loop until it passes. Do not show the spec to the user yet.

### Phase 6: User Approves Spec

Present the spec. Incorporate user edits until approved. If the edits are significant, re-run Phase 5. Do not proceed without explicit approval.

### Phase 7: Write the Full Plan

Dispatch `craft-planner` (inherit model — do not set `model`). Pass the spec, your context briefing from Phase 1, and the paths to the three reference files:

```text
Spec: docs/specs/<feature>.md

Context briefing:
<paste the synthesized context briefing from Phase 1>

Reference files:
- <path>/references/architecture-principles.md
- <path>/references/design-principles.md
- <path>/references/testing-principles.md
```

The planner reads the references, designs the architecture, writes all Tasks with literal code, writes tests, runs self-critique, and produces `docs/plans/<feature>.md`. Do **not** write the plan yourself — the planner handles all code-heavy work so your context stays light for later phases.

### Phase 8: Code Review Loop

Dispatch `craft-code-reviewer` over the **full plan**:

```text
Plan: docs/plans/<feature>.md
Spec: docs/specs/<feature>.md
```

If it returns Critical/High findings, **resume the planner agent** (pass its agent ID via `resume`) with the reviewer's findings and ask it to fix them — do not fix the plan yourself. The planner already has the full plan in context and can apply targeted fixes without re-reading everything.

Once the planner confirms fixes are applied, **resume the same reviewer agent** (pass its agent ID via `resume`) listing the changes — do not dispatch a new reviewer. The resumed reviewer already has the plan in context and only needs to verify the fixes.

Loop until no Critical/High findings remain. Use your judgment on Medium/Low findings — forward to the planner or consciously decline.

### Phase 9: User Approves Plan

Present the finished, pre-reviewed plan for holistic sign-off. Apply any last edits and wait for explicit approval.

### Phase 10: Implement

Dispatch one `craft-coder` per Task. You decide the parallelism: disjoint Tasks run concurrently in one message; dependent Tasks run in waves after their dependencies land.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

Implement the `## Tests` section **after** all Task waves land — dispatch a coder for it (or several, split by test file, e.g. `Your task: Tests 1–2 — implement these and no others.`).

For **manual subtasks**, pause and ask the user to execute them before dispatching dependent work.

### Phase 11: Validate

Once all Tasks and tests land, invoke the `craft-validation` skill to verify the implementation works and report results.
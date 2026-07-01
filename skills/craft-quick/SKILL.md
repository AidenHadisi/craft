---
name: craft-quick
description: Fast, single-gate workflow for straightforward tasks. Explores, plans, gets one approval, implements, and verifies. Use when the user says "craft-quick", asks for a quick implementation, or the task is simple enough that a full craft spec and review cycle would be overhead.
---

# craft-quick

The fast path for tasks that don't need craft's full discipline. Same quality bar for code, but no spec file, no design options, no review loops, one approval gate. The orchestrator writes the plan directly and runs verification inline.

**When to use craft-quick vs craft:**
- **craft-quick** — the approach is obvious, the scope is contained, and a single plan document is enough to align with the user.
- **craft** — the task has competing design options, touches many systems, or needs a spec to align on *what* before deciding *how*.

**Operating rules:**

- **Do not skip the user gate.** Present the plan and wait for explicit approval before implementing.
- **Don't stretch craft-quick.** If the task turns out to need a spec, multiple design options, or a code review loop, tell the user and suggest switching to craft.

## Subagents

| Subagent | Role | Model |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | `gemini-3.5-flash` |
| `craft-coder` | Implement assigned Tasks exactly | `gemini-3.5-flash` |

> Pass `model: gemini-3.5-flash` when dispatching both agents.
>
> **Always resume, never re-dispatch.** When you need more work from a subagent that has already completed, resume it by passing its agent ID via `resume`.

## Workflow Checklist

```markdown
- [ ] Phase 0: Restate the task
- [ ] Phase 1: Explore (optional)
- [ ] Phase 2: Write the plan
- [ ] Phase 3: User approves plan
- [ ] Phase 4: Implement (parallel craft-coder)
- [ ] Phase 5: Verify (build/test/lint)
```

### Phase 0: Restate the Task

In 1–2 sentences, state what the task is and what "done" looks like. Derive a short kebab-case `<feature>` slug.

### Phase 1: Explore

Optional. If the area is unfamiliar, dispatch `craft-explorer` agents in parallel (same as craft Phase 1) with `model: gemini-3.5-flash`:

```text
Slice: <focused area to investigate>
Starting points: <files/dirs/symbols if known, else "locate them yourself">
```

If you already have enough context from the conversation or can get it by reading a few files directly, skip the dispatch. Synthesize what you know into a short context briefing for yourself either way.

### Phase 2: Write the Plan

Read [references/architecture-principles.md](../craft/references/architecture-principles.md), [references/design-principles.md](../craft/references/design-principles.md), and [references/testing-principles.md](../craft/references/testing-principles.md) and apply them.

Write `docs/plans/<feature>.md` yourself using the same format as craft:

1. `## Architecture & design` — overview, Tasks table, data-flow diagram, design decisions.
2. `## Tasks` — all Tasks in dependency order, each with a design note and ordered subtasks containing complete literal code or manual actions.
3. `## Tests` — if the changes warrant tests. Skip for trivial changes and note why under `### Not tested`.
4. `## Verification` — the build/lint/test commands to run after implementation.

For simple tasks this will naturally be short — a single Task with a few subtasks is fine.

### Phase 3: User Approves Plan

Present the plan. Incorporate edits until approved. Do not proceed without explicit approval.

If the user's feedback reveals the task is more complex than expected (needs a spec, competing designs, or a code review loop), suggest switching to craft.

### Phase 4: Implement

Dispatch one `craft-coder` per Task with `model: gemini-3.5-flash`. Disjoint Tasks run concurrently; dependent Tasks run in waves.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

If the plan has a `## Tests` section, dispatch a coder for it after all Task waves land.

For **manual subtasks**, pause and ask the user to execute them before dispatching dependent work.

### Phase 5: Verify

Run the commands from the plan's `## Verification` section directly:

1. Build / typecheck.
2. Lint (use auto-fix if available, then re-check).
3. Run the tests written in the plan.

If something fails, fix it directly or report it to the user. No craft-validation skill, no API smoke tests, no browser checks.

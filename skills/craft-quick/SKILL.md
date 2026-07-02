---
name: craft-quick
description: Fast, single-gate workflow for building a feature. Explores, writes a directive-level plan, gets one approval, implements with parallel coders under heavy review, then verifies and live-tests the result. Use when the user says "craft-quick" or asks for a quick implementation.
---

# Craft Quick

You are an **autonomous senior developer**. You write the plan, dispatch coders to type the code, judge their work against a hard quality bar, and then prove the feature works by running it — not just reading it.

**Operating rules:**

- **One gate.** Present the plan and wait for explicit approval before implementing. Silence is not approval.
- **Review every wave.** Never accept coder output unread. You review the diffs, not the reports.
- **Never mutate prod.** Live testing runs locally. Stub side effects, use test data, and revert every temporary change before finishing.

## Subagents

| Subagent | Role | Model |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | `fast` |
| `craft-coder` | Implement assigned Tasks | `fast` |

> Pass `model: fast` on every dispatch.
>
> **Always resume, never re-dispatch.** When you need more work from a subagent that has already completed, resume it by passing its agent ID via `resume`.

## Workflow Checklist

```markdown
- [ ] Phase 0: Restate the task
- [ ] Phase 1: Explore (optional)
- [ ] Phase 2: Write the plan
- [ ] Phase 3: User approves plan
- [ ] Phase 4: Implement + review waves (craft-coder)
- [ ] Phase 5: Verify & live test
```

### Phase 0: Restate the Task

In 1–2 sentences, state what you're building and what "done" looks like. Derive a short kebab-case `<feature>` slug.

### Phase 1: Explore

Skip this phase if you already know the code you'll touch, or can learn it by reading a few files directly.

If the area is unfamiliar, dispatch one `craft-explorer` per slice **in parallel**, each with `model: fast`:

```text
Slice: <focused area to investigate>
Starting points: <files/dirs/symbols if known, else "locate them yourself">
```

Either way, write down the repo's conventions — naming, error handling, module boundaries, test patterns, libraries in use. This briefing goes into the plan's `## Conventions` section and gets pasted into every coder dispatch.

### Phase 2: Write the Plan

Read [design-principles.md](../craft/references/design-principles.md) and [testing-principles.md](../craft/references/testing-principles.md), then write `docs/plans/<feature>.md` yourself, mirroring the structure of [references/example-plan.md](references/example-plan.md):

1. `## Goal` — the problem and the requirements. A short paragraph plus requirement bullets; the plan must stand alone.
2. `## Approach` — 2–4 sentences: the shape of the change and why.
3. `## Conventions` — the repo's conventions from Phase 1, as bullets: error style, naming, module boundaries, test shape, libraries. Coders receive these verbatim.
4. `## Changes` — Tasks in dependency order, subtasks numbered `1.1`, `1.2`, … Each subtask names a file (`· create` / `· edit` / `· manual`) and describes the change in a few bullets.
5. `## Tests` — one plain-language case list per test file. Omit for trivial changes.
6. `## Verification` — the build/lint/test commands, plus the live tests that prove the feature works end to end.

Write directives, not code: say **where** and **what** precisely, and leave **how** to the coder. Include a contract or snippet only where precision matters — exact signatures, types, endpoints, schemas, or logic that's easy to get wrong.

### Phase 3: User Approves Plan

Present the plan. Incorporate edits until the user explicitly approves.

### Phase 4: Implement + Review Waves

Dispatch one `craft-coder` per Task with `model: fast`. Disjoint Tasks run concurrently in one message; dependent Tasks run in waves after their dependencies land.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
Conventions:
<paste the plan's ## Conventions section>
```

For `· manual` subtasks, pause and ask the user to execute them before dispatching dependent work.

**Review each wave before dispatching the next.** Read the changed files or `git diff` yourself — coder reports are claims, not evidence. Judge against the design-principles you read in Phase 2:

- **Contracts** — signatures, types, endpoints match the plan exactly.
- **Conventions** — naming, error style, imports, test shape match the plan's `## Conventions`.
- **Concise** — less code is better; no unnecessary helpers, wrappers, or single-implementation interfaces. If a coder wrote 60 lines where 20 do, send it back.
- **Modern** — the language's current features and established, well-maintained packages instead of hand-rolling (dates, retries, validation, parsing, HTTP). A hand-rolled utility with a popular library equivalent is a review failure.
- **Clean code** — functions do one thing at one level of abstraction; guard clauses over nesting; intention-revealing names; command–query separation; no swallowed errors; comments explain why, not what.
- **Patterns & smells** — design patterns only where they remove real complexity (strategy vs a function parameter, factory vs a literal); classic smells get sent back: duplicated logic, feature envy, shotgun surgery, primitive obsession, long parameter lists, leaky abstractions.
- **Boundaries** — the plan's task seams respected; dependencies point one way; consumers own their abstractions.

If a coder's work fails review, **resume that coder** with specific corrections — file, problem, required fix (e.g. "in `store.go`, inline the single-use `validateName` helper; error wrapping here is `fmt.Errorf` with `%w`"). Re-review when it reports back. Only dispatch the next wave when the current one passes.

### Phase 5: Verify & Live Test

**Part A — Static.** Run the commands from the plan's `## Verification` section:

1. Build / typecheck.
2. Lint — auto-fix if available, then re-check.
3. Tests.

Fix failures directly, or report them to the user if the fix isn't obvious.

**Part B — Live.** Read [references/live-testing.md](references/live-testing.md) and follow it. Prove the feature works by running it:

1. **Run the app locally** — discover the dev setup from `package.json` scripts, `Makefile`, `docker-compose.yml`, README.
2. **Get credentials** — from wherever the project keeps them: `.env` files, AWS Secrets Manager, config files.
3. **Test the feature end to end** — call the new endpoints with real requests; exercise the real flow.
4. **Frontend** — use the Cursor browser to navigate and test the pages the feature touches. If blocked by a login page, ask the user to log in, then continue.
5. **Revert all temporary changes** (stubs, auth bypasses) and report what was tested and how.

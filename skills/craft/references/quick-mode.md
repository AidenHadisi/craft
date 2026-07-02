# Quick Mode

**One gate.** The user explicitly approves the plan before you implement.

## Artifact

Derive a kebab-case `<feature>` slug. You produce one artifact: **`docs/plans/<feature>.md`** — a directive-level plan, written by you.

## Steps

```markdown
- [ ] 1. Restate the task
- [ ] 2. Explore
- [ ] 3. Write the plan
- [ ] 4. Get plan approval (gate)
- [ ] 5. Implement + review waves
- [ ] 6. Verify & live test
```

### 1. Restate the Task

State in 1–2 sentences what you're building and what "done" looks like. Derive the `<feature>` slug.

### 2. Explore

Dispatch one `craft-explorer` per slice of the codebase, in parallel:

```text
Slice: <focused area to investigate>
Starting points: <files/dirs/symbols if known, else "locate them yourself">
```

Skip only when the conversation already gives you everything the plan needs.

From the reports, write down the repo's conventions — naming, error handling, module boundaries, test patterns, libraries. This becomes the plan's `## Conventions` section.

### 3. Write the Plan

Read [design-principles.md](design-principles.md) and [testing-principles.md](testing-principles.md), then write `docs/plans/<feature>.md`, mirroring the structure and level of [example-plan-quick.md](example-plan-quick.md).

Write directives, not code: say **where** and **what** precisely; leave **how** to the coder. Include a contract or snippet only where precision matters — signatures, types, endpoints, schemas, tricky logic.

### 4. Get Plan Approval (gate)

Present the plan. Incorporate edits until the user explicitly approves.

### 5. Implement + Review Waves

Dispatch one `craft-coder` per Task. Disjoint Tasks go out concurrently; dependent Tasks run in waves.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
Conventions:
<paste the plan's ## Conventions section>
```

For `· manual` subtasks, pause and ask the user to execute them first.

**Review each wave before dispatching the next.** Read the diffs yourself and judge:

- **Contracts** — signatures, types, endpoints match the plan exactly.
- **Conventions** — naming, error style, imports, test shape match the plan.
- **Concise** — less code is better. No unnecessary helpers, wrappers, or single-implementation interfaces. 60 lines where 20 do gets sent back.
- **Modern** — current language features and established packages over hand-rolling (dates, retries, validation, parsing, HTTP).
- **Clean code** — one thing per function, guard clauses over nesting, intention-revealing names, no swallowed errors, comments explain why.
- **Patterns & smells** — patterns only where they remove real complexity; send back duplicated logic, feature envy, shotgun surgery, primitive obsession, long parameter lists, leaky abstractions.
- **Boundaries** — task seams respected; dependencies point one way; consumers own their abstractions.

On failure, resume that coder with specific corrections — file, problem, required fix. Re-review. Next wave only when the current one passes.

### 6. Verify & Live Test

**Static.** Run the plan's `## Verification` commands: build, lint (auto-fix then re-check), tests. On failure, resume the coder that owns the affected files with the error output; fix directly only if it's a one-liner.

**Live.** Read [live-testing.md](live-testing.md) and follow it:

1. Run the app locally — discover the dev setup (`package.json`, `Makefile`, `docker-compose.yml`, README).
2. Get credentials from wherever the project keeps them — `.env`, AWS Secrets Manager, config files.
3. Exercise the feature end to end with real requests.
4. Frontend: test the pages with the Cursor browser. If blocked by a login, ask the user to log in, then continue.
5. Revert all temporary changes (stubs, auth bypasses) and report what was tested and how.

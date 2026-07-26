# Quick Mode

**Two gates.** The user explicitly approves the design choice before you write the plan, and the plan before you implement.

## Artifact

Derive a kebab-case `<feature>` slug. You produce one artifact: `docs/plans/<feature>.md` — a directive-level plan, written by you.

## Steps

```markdown
- [ ] 1. Restate the task
- [ ] 2. Explore
- [ ] 3. Interview the user
- [ ] 4. Design options — user picks (gate)
- [ ] 5. Write the plan
- [ ] 6. Plan review loop
- [ ] 7. Get plan approval (gate)
- [ ] 8. Implement + review waves
- [ ] 9. Polish
- [ ] 10. Live test
```

### 1. Restate the Task

State in a few sentences what you're building and what "done" looks like. Derive the `<feature>` slug.

### 2. Explore

Dispatch one `craft-explorer` per slice of the codebase, in parallel.

```text
Slice: <focused area to investigate>
Starting points: <files/dirs/symbols if known, else "locate them yourself">
```

Skip only when the conversation already gives you everything the plan needs.

From the reports, write down the repo's conventions — naming, error handling, module boundaries, test patterns, libraries. This becomes the plan's `## Conventions` section.

### 3. Interview the User

Before writing anything, surface the decisions the plan would otherwise assume: scope boundaries, behavior on edge cases, UX choices, what to do with existing data or callers. Ask **one question at a time**, each with a recommended answer. If a question can be answered by reading the code, dispatch a subagent to answer it instead of asking. Skip only when exploration left no real decisions open.

If the work would benefit from a third-party package or tool the repo doesn't already use — and a robust, modern, popular option exists — ask which to use as one of these questions, with your recommendation and why (maturity, adoption, maintenance, fit with the existing stack). Don't ask when the repo already has an established choice for the need; use that instead.

### 4. Design Options

Present the recommended approach first — one line on what it is and why it wins — then 2–3 genuinely different viable alternatives with one-line trade-offs. Fewer if none are genuinely viable; never invent fake alternatives. For truly mechanical tasks with one sensible shape, state the approach and ask to proceed. The user picks or composes a hybrid.

### 5. Write the Plan

Read [design-principles.md](design-principles.md) and[testing-principles.md](testing-principles.md) — plus [architecture-principles.md](architecture-principles.md) when the plan will have 2+ Tasks — then write `docs/plans/<feature>.md`, mirroring the structure and level of [example-plan-quick.md](example-plan-quick.md).

The plan must read top-down at a glance. `## Goal` carries the problem and requirements — there is no spec, so it must stand alone. Every Task opens with one sentence on what it delivers and a **Done when:** acceptance line; every subtask is a bolded one-sentence headline saying **what**, with the file path and action on a quiet line below. Add detail bullets under a subtask only where the coder would otherwise guess wrong — an exact signature, endpoint, schema, or tricky rule. Most subtasks need none. Deliberate exclusions go in `## Out of scope`; shapes shared by 2+ Tasks go in `## Contracts` (signatures, types, endpoints, wire shapes only — never bodies or prose). Leave **how** to the coder, and never write code beyond a short contract.

**Self-review before presenting.** Check and fix inline:

- Every requirement in `## Goal` maps to a subtask.
- Contracts referenced by later Tasks match where they're defined.
- Edge cases and failure modes surfaced in the interview appear in a Task or in `## Out of scope`.
- Nothing violates the design principles' don't-list.



### 6. Plan Review Loop

Dispatch `craft-reviewer`:

```text
Artifact: docs/plans/<feature>.md — a directive plan, no literal code.

Reference files:
- <path>/references/design-principles.md
- <path>/references/architecture-principles.md
- <path>/references/testing-principles.md
```

If it returns `Needs changes`, apply the Must-fix feedback and resume it to re-check. Loop until it passes. Do not show the plan to the user yet.

### 7. Get Plan Approval (gate)

Present the pre-reviewed plan. Incorporate edits until the user explicitly approves. If the edits are significant, re-run the review loop.

### 8. Implement + Review Waves

Dispatch one `craft-coder` per Task. Disjoint Tasks go out concurrently; dependent Tasks run in waves.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
Conventions:
<paste the plan's ## Conventions section>
```

For `manual` subtasks, pause and ask the user to execute them first.

**Review each wave before dispatching the next.** Read the diffs yourself and judge:

- **Contracts** — signatures, types, endpoints match the plan exactly.
- **Conventions** — naming, error style, imports, test shape match the plan.
- **Concise** — less code is better. No unnecessary helpers, wrappers, or single-implementation interfaces. 60 lines where 20 do gets sent back.
- **Modern** — current language features and established packages over hand-rolling (dates, retries, validation, parsing, HTTP).
- **Clean code** — one thing per function, guard clauses over nesting, intention-revealing names, no swallowed errors, comments explain why.
- **Patterns & smells** — patterns only where they remove real complexity; send back duplicated logic, feature envy, shotgun surgery, primitive obsession, long parameter lists, leaky abstractions.
- **Boundaries** — task seams respected; dependencies point one way; consumers own their abstractions.

On failure, resume that coder with specific corrections — file, problem, required fix. Re-review. Next wave only when the current one passes.

### 9. Polish

Run the plan's `## Verification` commands first — build, lint (auto-fix then re-check), tests. On failure, resume the coder that owns the affected files with the error output; fix directly only if it's a one-liner.

Once static checks pass, dispatch `craft-polisher` (inherit model — do not set `model`):

```text
Plan: docs/plans/<feature>.md
Files changed: <list of files, or "diff against <base>">
Conventions:
<paste the plan's ## Conventions section>
```

The polisher reads the architecture and design standards itself. It may restructure within the feature's footprint. Review its diff with the same wave lens, then re-run the full `## Verification` commands. Skip this step only when the diff is trivially small.

### 10. Live Test

Invoke the **craft-test** skill ([../../craft-test/SKILL.md](../../craft-test/SKILL.md)) and follow it end to end — run locally, instrument, exercise the feature, revert, report.

---
name: craft-validation
description: Verify that code works after implementation. Ensures docs/validation.md exists, then runs build, test, lint, API smoke tests, and frontend browser checks with a self-healing fix loop. Use after craft finishes, standalone before a deploy, or whenever you need to verify a project works.
---

# Craft Validation

Verify the project builds, passes tests, responds to API calls, and renders in the browser.

**Rules:**

- If `docs/validation.md` does not exist, build it first (Step 1).
- Get explicit user approval before writing `docs/validation.md`.
- Run commands from the validation doc — do not guess.
- Never call endpoints with side effects (emails, webhooks, deletes).

## Subagents

| Subagent | Role | Model |
|---|---|---|
| `craft-onboard-explorer` | Discover one slice of validation infrastructure | `fast` |
| `craft-coder` | Fix build/test/lint failures | `fast` |

## Workflow

### Step 1: Ensure `docs/validation.md` exists

If it exists, skip to Step 2.

If not:

1. Read [references/discovery.md](references/discovery.md) for the explorer slices.
2. Dispatch one `craft-onboard-explorer` per slice **in parallel** with `model: fast`.
3. Synthesize into a draft following [references/example-validation.md](references/example-validation.md).
4. Present to the user. Incorporate edits until approved, then write the file.

### Step 2: Run validation

Read `docs/validation.md` and execute in order:

1. **Build & typecheck** — run the commands from the doc.
2. **Lint** — run lint commands. Use auto-fix if available, then re-check.
3. **Unit tests** — run the test command.
4. **API smoke tests** — read [references/backend.md](references/backend.md), retrieve credentials per the doc's Authentication section, execute each curl command from the smoke test table.
5. **Frontend** — read [references/frontend.md](references/frontend.md), open each page from the doc's Frontend table in a browser. Ask the user to log in if needed. Skip if the project has no frontend.

### Step 3: Self-healing

When build, lint, or tests fail:

1. Dispatch a `craft-coder` with the error output and the doc's "Common failures" section.
2. Re-run the failed step.
3. Loop up to **3 times**. Stop and report if still failing.

API and frontend failures are not self-healed — report them directly.

### Step 4: Report

```markdown
## Validation report

### Results
- [ ] Build
- [ ] Typecheck
- [ ] Lint
- [ ] Unit tests
- [ ] API smoke tests
- [ ] Frontend

### Failures
- <step> — <error summary>

### Fixes applied
- <what changed, if any>
```

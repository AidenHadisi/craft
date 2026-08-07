# Testing Principles

How to design the plan's `## Tests` section. Cover important behavior; skip the rest; write cases the repo would write.

## What to cover

Cover business logic, contracts between Tasks, and the edge cases / failure modes named in `## Requirements`. Skip code that is obviously correct at a glance: trivial getters, framework glue, generated code, pass-through wiring. `### Not tested` lists only meaningful planned behavior intentionally omitted, each with a reason — not every trivial getter or glue line.

## Repo idioms

Use the explorer's findings: framework, file location and naming, test shape, fixture style. Never introduce a new test framework or pattern when the repo already has one.

## Mocking

- Mock only real external boundaries — DB, HTTP, queues, clocks, filesystems — and nothing else.
- Reuse the project's existing mocking approach exactly. Never hand-roll a second mocking style beside an established one.
- Pure logic is tested directly, with no mocks.
- Do not alter production architecture solely to make tests mockable. Use existing seams or test through public behavior.

## Cases

Every case is one plain-language bullet under its file ("rejects a blank name without creating an entry"). Never cram several behaviors into one line. The coder mirrors these one-to-one as test case names.

**Oracle.** Every case asserts an observable outcome — return value, state, status, error, or rendered result. Execution alone, coverage alone, or mock-call verification alone is not an oracle.

## Don't over-test

One test per behavior, not per line. No tests that re-assert the type system. No duplicate coverage of the same branch. A test that could only fail if the compiler or framework broke is a test to delete.

## Tests Section Template

Add to `docs/plans/<feature>.md`, between Tasks and `## Verification`:

```markdown
## Tests

- [path/to/foo_test.go](path/to/foo_test.go) — table-driven with a hand-rolled fake store.
  - A valid save returns 201 with the stored row.
  - A blank name returns 400 and never reaches the store.
  - A store failure surfaces as 500.

### Not tested
- <meaningful planned behavior> — <why omitted>
```

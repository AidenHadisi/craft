# Testing Principles

How to design the plan's `## Tests` section. The bar: every important behavior is covered, nothing trivial is, and the tests read like the repo wrote them. Work through the sections in order, then run the self-critique before presenting.

## 1. Test what matters, skip the rest

Cover business logic, contracts between Tasks, and the edge cases / failure modes named in the spec.

**Not everything needs a test.** Code that is simple and reliable enough to be obviously correct at a glance earns no test: trivial getters, framework glue, generated code, pass-through wiring, straight-line mapping. The default for such code is *skip*, not "cover it just in case."

Every skip is an explicit decision: list it under `### Not tested` with a reason. Silence is not a decision.

## 2. Follow the repo's testing idioms

Use the context briefing's findings: framework, file location and naming, test shape, fixture style. Go gets table-driven tests with `t.Run`; other languages get their idiomatic equivalent. Never introduce a new test framework or pattern when the repo already has one.

## 3. Mock at real boundaries only

- Mock external dependencies — DB, HTTP, queues, clocks, filesystems — and nothing else.
- Reuse the project's existing mocking approach exactly (mockery, testify mocks, MSW, hand-rolled fakes — whatever the explorer found). Never hand-roll a second mocking style next to an established one.
- Pure logic is tested directly, with no mocks.

## 4. Plain-language case list

Each test file's subsection starts with a `Covers:` bullet list — one line per case, in plain language, describing the behavior it verifies ("rejects a blank name without creating an entry"). Test case names in the code mirror these lines, so anyone can map prose to test and back.

## 5. Don't over-test

- One test per behavior, not per line.
- No tests that re-assert the type system.
- No mock-verification-only tests that just confirm the code calls what it calls.
- No duplicate coverage of the same branch.
- A test that could only fail if the compiler or framework broke is a test to delete.

## Tests Section Template

Add this section to `docs/plans/<feature>.md`, between `## Tasks` and `## Verification`. One subsection per test file, with complete literal code a coder can reproduce verbatim.

```markdown
## Tests

### Test 1 — <area under test>   (covers: Task N)
[path/to/foo_test.go](path/to/foo_test.go) · create

Covers:
- <plain-language behavior this case verifies>
- <...>

```go
<complete literal test code>
```

### Not tested
- <area> — <reason it doesn't earn a test>
```

## Self-Critique

Argue against your test design before presenting it:

- **Important logic covered?** Every spec-named behavior and failure mode has a case.
- **Trivial code left alone?** No tests on glue, wiring, or obviously-correct code.
- **Mocks only at boundaries?** Nothing mocked that isn't an external dependency; the repo's mock style reused exactly.
- **Cases readable?** The `Covers:` list explains each test in plain language, and code names mirror it.
- **Zero decisions left?** A coder could implement every test file verbatim.

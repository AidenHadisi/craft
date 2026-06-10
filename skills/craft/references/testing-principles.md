# Testing Principles

How to design a Task's tests (Phase 9, alongside the design principles). The goal: every important behavior is verified, nothing trivial is, and the tests read like the repo wrote them. Tests are subtasks in the plan — complete literal code, approved at the same gate as the implementation.

## 1. Test what matters

Tests earn their place the same way code does. Cover:

- **Business logic** — decisions, calculations, transformations. The reason the feature exists.
- **Contracts between Tasks** — the public surface downstream Tasks build on.
- **Edge cases and failure modes named in the spec** — each key scenario in the spec maps to at least one test.

Skip: trivial getters/setters, framework glue, generated code, pass-through wiring, configuration. If a Task has no logic worth testing (pure wiring, manual actions), say so explicitly in its design note — "No tests: <reason>." Silence is not a decision.

## 2. Follow the repo's testing idioms

The explorer reports how this repo tests: framework, file layout, naming, fixture style, assertion library. Match all of it — a test that fights the house style is a defect even when it passes.

- Go gets table-driven tests with `t.Run` per case; other languages get their idiomatic equivalent (parameterized tests, `describe`/`it` blocks, pytest fixtures).
- Put test files where the repo puts them, named how the repo names them.
- Never introduce a new test framework, assertion library, or pattern when the repo already has one.
- Greenfield repo with no tests yet? Use the language's standard idiom and the most boring, mainstream tooling.

## 3. Mock at real boundaries — and only there

- Mock external dependencies: database, HTTP services, queues, clocks, filesystem, randomness. These make tests slow, flaky, or environment-dependent.
- **Reuse the project's existing mocking approach exactly** — generated mocks (mockery, GoMock), MSW handlers, testify mocks, hand-rolled fakes, whatever the explorer found. Never hand-roll a second mocking style next to an established one.
- Pure logic is tested directly with real values and no mocks. If a test needs heavy mocking to reach plain logic, that is a design smell — revisit the seam, don't pile on mocks.

## 4. Plain-language case list

Every test subtask starts with a bullet list — one line per test case, in plain language, describing the behavior it verifies:

```markdown
Covers:
- saves a search and returns it with a generated id
- rejects a blank name without creating an entry
- saving a duplicate name replaces the existing entry instead of adding one
```

The case names in code mirror these lines (table-test `name` fields, `it("...")` strings). A reader should understand what the Task guarantees by reading the list alone.

## 5. Don't over-test

One test per behavior, not per line. Never write:

- Tests that re-assert the type system or the framework (a struct holds what you put in it).
- Mock-verification tests that only confirm the code calls what it obviously calls.
- Duplicate coverage of the same branch through slightly different inputs.
- Tests of private internals that a public-surface test already exercises.

A small, sharp suite that fails loudly on real regressions beats a large one that drowns them in noise.

## Self-Critique

Before presenting a Task's tests:

- **Important paths covered?** Every spec-named scenario and failure mode for this Task has a test.
- **Anything trivial tested?** Cut tests that can't fail for a real reason.
- **Mocks only at boundaries?** No mocks around pure logic; no second mocking style.
- **Idiomatic?** Shape, naming, and placement match the explorer's findings.
- **Case list honest?** Every bullet maps to a real test case, and vice versa.

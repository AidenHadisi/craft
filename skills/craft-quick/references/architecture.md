## Standards

These standards bind everyone who designs, writes, reviews, or polishes code for this work. They describe the shape good code has here; each role's brief says what to do when the code falls short.

### The ladder

Walk this list in order for every piece of code, and stop at the first yes:

1. Does this need to exist? → no: skip it (YAGNI)
2. Already in this codebase? → reuse it, don't rewrite
3. Stdlib does it? → use it
4. Native platform feature? → use it
5. Installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that works

### Cut

- Each piece of work owns one job. If you cannot name that job, the cut is wrong.
- The deletion test: delete a piece — if complexity vanishes it was a pass-through; if it reappears across its callers it earned its keep.
- One implementation means no interface. Do not introduce a second abstraction until a second real implementation exists.
- Dependencies flow one way. No cycles.
- Prefer fewer deep pieces over many shallow ones.
- Earn every new layer, package, or interface by naming what it buys today. Any deviation from the simplest shape says why the simpler one was rejected.
- Shape for the next change. Where a kind of thing will clearly grow — more fields, variants, handlers, callers — pick the shape where adding one is a new entry, not edits in several places: data over branching, one generic path over copies, a table or map over a chain of ifs. This is a choice of shape, not extra code; if it costs more code or a new layer today, YAGNI wins.

### Code

- The least code that stays clear: no speculative generality, no config knobs nobody asked for, no helpers without real duplication, no validation of internal typed code, no guards for impossible cases.
- Idiomatic and modern for the language and its version in this repo; shaped like its neighbors; readable top to bottom.
- Repo conventions beat personal preference. Mirror a nearby sibling feature before inventing structure.
- Prefer well-maintained existing solutions — stdlib, dependencies already installed, a well-maintained package — over hand-rolling.
- Errors are handled, not swallowed.
- Verify unfamiliar APIs, symbols, and config against the repo or authoritative docs; never invent by analogy.
- Stay inside the requested behavior. No drive-by refactors or tidying.
- Tests assert one observable outcome each, named after the criterion they prove; tests that only exercise code or check mock calls are not tests.

## Process

Start from repo facts you already have; read the repo only for what they do not cover. Every file, convention, and exemplar you name must be real.

1. **List the jobs:** persist X, expose Y, render Z, …
2. **Fit them to the repo** — files to change, sibling to mirror, package or stdlib instead of hand-rolled code.
3. **Cut into steps** in dependency order. A small feature can be one step. Do not invent steps for setup, plumbing, or wiring that aren't real work.
4. **Write each step** so a coder can build it without guessing and without adding anything.

## Write

Steps go under `## Steps` in the plan file, one `### N. <short title>` each. No Components, Seams, Key decisions, or Slices headings.

Each step names the files, the sibling to mirror, and the edge and error paths, then shows every piece of code it adds: full code for signatures, types, schemas, queries, and non-obvious logic; pseudocode only where the code is mechanical. The step fixes both the design and the amount of code. If the coder would have to choose a name, a shape, or whether to add a helper, the step is not done. Cut words, never information.

Tests go under `## Tests`, one short title per bullet, one behavior each. Tests are written in the step that owns them, not a separate step.

A small feature is one or two steps.

Filled example (do not copy the domain; copy the density):

````md
## Steps

### 1. Accept an optional `filter` query param

In `internal/audit/handler.go`, read `filter` from the query string and pass it on the existing list params, mirroring `internal/events/handler.go`. Unknown params stay ignored; empty means no filter.

```go
type ListParams struct {
    Limit  int
    Filter string // optional; case-insensitive substring on Message
}

// in List, after the existing limit parsing:
params.Filter = r.URL.Query().Get("filter")
```

### 2. Apply the filter in the store

In `internal/audit/store.go`, extend the existing query builder. Same empty-list JSON as today when nothing matches. No new index. Add both tests to `internal/audit/handler_test.go`.

```go
if p.Filter != "" {
    args = append(args, p.Filter)
    where = append(where, fmt.Sprintf("message ILIKE '%%' || $%d || '%%'", len(args)))
}
```

## Tests

- filters by message substring
- empty filter returns all
````

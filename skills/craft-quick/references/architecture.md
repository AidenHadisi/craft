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
3. **Cut into tasks** in dependency order. A small feature can be one task. Do not invent tasks for setup, plumbing, or wiring that aren't real work.
4. **Write each task** so a coder can build it without guessing.

## Write

The architecture is a numbered list of tasks. No Components, Seams, Key decisions, or Slices headings.

Each task is a title plus a short body. Name the files, the sibling to mirror, and the edge and error paths in a line or two. Put a schema, signature, or short pseudocode in a code block when a later task or the coder would otherwise guess. Cut words, never information.

A small feature is one or two tasks.

Use this shape:

````md
1. **<task title>**

<What to do, in which files. Mirror `<sibling path>` when there is one. Edges and errors in a line or two.>

```ts
<schema, signature, or pseudocode — only when it pins something>
```

2. **<next task title>**

<…>

**Checks:** `<lint / typecheck / test command>`
````

Filled example (do not copy the domain; copy the density):

````md
1. **Accept an optional `filter` query param**

In `internal/audit/handler.go`, read `filter` from the query string and pass it on the existing list params. Mirror `internal/events/handler.go`. Unknown params stay ignored; empty means no filter.

```go
type ListParams struct {
    Limit  int
    Filter string // optional; case-insensitive substring on Message
}
```

2. **Apply the filter in the store**

In `internal/audit/store.go`, when `Filter` is non-empty, add `WHERE message ILIKE '%' || $n || '%'`. Same empty-list JSON as today when nothing matches. No new index.

3. **Test the query**

In `internal/audit/handler_test.go`: `filters by message substring` and `empty filter returns all`.

**Checks:** `go test ./internal/audit/...`
````

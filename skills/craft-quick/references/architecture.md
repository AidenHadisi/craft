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
2. **Fit them to the repo** — relevant files, examples to follow, and package or stdlib choices where useful.
3. **Cut into steps** in dependency order. A small feature can be one step. Do not invent steps for setup, plumbing, or wiring that aren't real work.
4. **Explain each step** with enough implementation detail for the coder to understand the intended change; use the level of detail the task needs.

## Write

Keep each quick task's plan in `.craft/<task>/plan.md`. Start from the [plan template](../assets/templates/plan.md) and adapt its four sections: Progress, Architecture, Implementation, and Testing. This single file is the resume entry and records workflow state, approval, critic rulings, step status, and check results. Keep shared repo guidance in the root guides; task-specific planning belongs in the task plan.

In Architecture, state the request, done criteria, constraints, exclusions, and chosen approach. In Implementation, use numbered steps and substeps in build order to explain the concrete changes and how they work. Choose prose, code snippets, pseudocode, schemas, queries, or logic as appropriate. Include relevant edge and error behavior where useful; adapt the outline to the task rather than repeating fixed fields. A small feature can be one step.

In Testing, list automated checks with commands and expected observable outcomes, then record what ran and the result. Identify each check by the behavior it proves. Tests belong with the implementation work they verify; do not invent a separate implementation step just for tests. There is no spec or live-test stage in Craft Quick.

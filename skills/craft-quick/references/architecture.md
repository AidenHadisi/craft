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

Keep the quick plan in `.craft/<task>/architecture.md`, `implementation.md`, and `testing.md`; record workflow state in `progress.md`. Start with the [progress](../assets/templates/progress.md), [architecture](../assets/templates/architecture.md), [implementation](../assets/templates/implementation.md), and [testing](../assets/templates/testing.md) templates, then adapt their headings and layout. They are concise starting shapes, not schemas; keep the conventional filenames and each document’s responsibility.

In `architecture.md`, state the request, what done looks like, constraints, out-of-scope items, and chosen design. In `implementation.md`, list only real steps in dependency order. Each step names owned files, a real sibling to mirror, relevant edge and error paths, and all the code it adds: full code for signatures, types, schemas, queries, and non-obvious logic; pseudocode only where work is mechanical. The step fixes the design and amount of code. If the coder must choose a name, shape, or whether to add a helper, the step is not done. A small feature can be one step. Keep its status in `progress.md`.

In `testing.md`, list automated checks with commands and expected observable outcomes, then record what ran and the result. Identify each check by the behavior it proves. Tests belong in the implementation step that owns them; do not invent a separate implementation step just for tests. There is no spec or live-test stage in Craft Quick.

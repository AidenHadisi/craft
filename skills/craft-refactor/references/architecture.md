## Standards

These standards bind everyone who designs, writes, reviews, or polishes code for this work. They describe the shape good code has here; each role's brief says what to do when the code falls short.

### The ladder

Walk this list in order for every component, seam, and piece of code, and stop at the first yes:

1. Does this need to exist? → no: skip it (YAGNI)
2. Already in this codebase? → reuse it, don't rewrite
3. Stdlib does it? → use it
4. Native platform feature? → use it
5. Installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that works

### Cut

- Each component owns one clear job and hides one changeable decision behind a small interface. If you cannot name that decision, the cut is wrong.
- The deletion test: delete a component — if complexity vanishes it was a pass-through; if it reappears across its callers it earned its keep.
- One implementation means no interface. Do not introduce a seam until a second real implementation exists.
- Dependencies flow one way. No cycles.
- Prefer fewer deep components over many shallow ones.
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
2. **Cut into components** until each owns one job (see Cut). Independent when either can change without rewriting the other. A small feature can be one component.
3. **Name the seams** — what crosses, which way. No cycles.
4. **Fit each to the repo** — files, sibling to mirror, package or stdlib instead of hand-rolled code.
5. **Slice** — smallest standalone unit that can be committed; order by dependency; union of slice criteria covers the spec; pin shared contracts in the slice that introduces them.

## Write

Two altitudes: **Components, Seams, Key decisions** stay at design altitude. **Slices** carry what a coder with zero context needs — one fact or decision per line, contracts in code blocks, tables for anything enumerable, pseudocode only for a genuinely non-obvious path. Cut words, never information.

Use exactly these headings. Each `###` heading is a slice, the first line under it is the slice's goal, and the bullets under `**Criteria:**` are its criteria.

````md
## Components

- **<name>** — <the one job it owns>. Files: `<path>`, `<path>`. Mirrors `<sibling path>` when there is one.

## Seams

- <from> → <to>: <what crosses>

## Key decisions

- <decision> — <why, one line>

## Slices

### 1. <short title>

<One sentence: what this slice delivers and which component(s) it builds.>

1.1 <One piece of the work: what it does, in which file.>

```ts
<the contract it pins — signature, endpoint, wire shape, error — when a later slice depends on it>
```

1.2 <Next piece, including its edge and error paths.>

**Criteria:**

- <observable behavior a branch review can check in the diff or a tester can run>

**Tests:**

- <one named behavior, one line, asserting one observable outcome>
````

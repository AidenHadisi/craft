These standards bind everyone who designs, writes, reviews, or polishes code for this feature. They describe the shape good code has here; each role's brief says what to do when the code falls short.

### The ladder

Walk this list in order for every component, seam, and piece of code, and stop at the first yes:

1. Does this need to exist? → no: skip it (YAGNI)
2. Already in this codebase? → reuse it, don't rewrite
3. Stdlib does it? → use it
4. Native platform feature? → use it
5. Installed dependency? → use it
6. One line? → one line
7. Only then: the minimum that works

### Design

- Each component owns one clear job and hides one changeable decision behind a small interface. If you cannot name that decision, the cut is wrong.
- The deletion test: delete a component — if complexity vanishes it was a pass-through; if it reappears across its callers it earned its keep.
- One implementation means no interface. Do not introduce a seam until a second real implementation exists.
- Dependencies flow one way. No cycles.
- Prefer fewer deep components over many shallow ones.
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

## Design

Design the shape that meets the approved spec, then cut it into slices a coder can build one at a time. Hold every component, seam, and slice to the Standards. Start from Findings; read the repo only for what they do not cover, and record it. Every file, convention, and exemplar you name must be real.

1. **List the jobs** the feature has: persist X, expose Y, render Z, …
2. **Cut into components** until each owns one clear job and hides one changeable decision. Two components are independent when either can change without rewriting the other. A small feature can be one component.
3. **Name the seams** — for each dependency, what crosses it and which way it flows. No cycles.
4. **Fit each component to the repo** — which files it touches, which sibling it mirrors, which existing package or stdlib feature it uses instead of hand-rolled code.

## Slice

- Each slice is the smallest standalone unit that can be committed and, where runnable, exercised on its own. Wiring finished pieces together counts as a slice.
- Order by dependency: smallest and most foundational first. Slices are numbered in the order written.
- The union of all slice criteria covers every criterion in the spec; the last slice usually completes the wiring.
- Pin every contract two slices must agree on — signature, endpoint, wire shape, error — in the slice that introduces it, so later coders do not invent their own.
- Aim for the fewest slices that keep each one a coherent commit.

## Write

Two altitudes:

- **Components, Seams, Key decisions** stay at design altitude: pieces, ownership, data flow, repo fit.
- **Slices** carry what a coder with zero context needs and nothing a coder can decide alone. Each slice has two readers — a coder who needs every detail and a user verifying each decision in one quick read — so one fact or decision per line, contracts in code blocks, tables for anything enumerable, pseudocode only for a genuinely non-obvious path. Cut words, never information.

Do not repeat repo conventions or how to run the project; they live in Conventions and Verification on the plan.

Use exactly these headings. Each `###` heading is a slice, the first line under it is the slice's goal, and the bullets under `**Criteria:**` are its criteria — keep that shape.

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

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

- Each piece of work owns one clear job.
- The deletion test: delete a piece — if complexity vanishes it was a pass-through; if it reappears across its callers it earned its keep.
- One implementation means no interface. Do not introduce an abstraction until a second real implementation exists.
- Dependencies flow one way. No cycles.
- Prefer fewer deep pieces over many shallow ones.
- Earn every new layer, package, or helper by naming what it buys today.
- Shape for the next change. Where variants or cases will clearly grow, choose data over branching, or a map/table over chained ifs. If it costs more code or layers today, YAGNI wins.

### Code

- The least code that stays clear: no speculative generality, no config knobs nobody asked for, no helpers without real duplication, no validation of internal typed code, no guards for impossible cases.
- Idiomatic and modern for the language and its version in this repo; shaped like its neighbors; readable top to bottom.
- Repo conventions beat personal preference. Mirror a nearby sibling feature before inventing structure.
- Prefer well-maintained existing solutions — stdlib, dependencies already installed, or established packages (informed by web research) — over hand-rolling.
- Errors are handled, not swallowed.
- Verify unfamiliar APIs, symbols, and config against authoritative docs or the repo; never invent by analogy.
- Stay inside the requested behavior. No drive-by refactors or tidying.
- Tests assert one observable outcome each, named after the behavior they prove; tests that only exercise code or check mock calls are not tests.

## Process

Start from repo facts and web research in Findings; read the repo only for what they do not cover. Every file, convention, and exemplar you name must be real.

1. **Architecture Overview:** Write a concise summary of the chosen design, how pieces fit together, and why this design was picked.
2. **Fit to the repo:** files to change/create, sibling to mirror, package or stdlib instead of hand-rolled code.
3. **Cut into steps:** in dependency order. A small feature can be one or two steps. Do not invent steps for setup, plumbing, or wiring that aren't real work.
4. **Write each step:** so a coder can build it without guessing or designing on the fly.
5. **List tests:** specific behaviors to verify.

## Write

Use `## Architecture Overview`, `## Steps`, and `## Tests`. No Components, Seams, Key decisions, or Slices headings.

- **Architecture Overview** gives the high-level picture: the chosen approach, how the parts interact, and why this design was chosen.
- Each step under `## Steps` is a `### N. <short title>` heading. It names the files, the sibling to mirror, edge/error paths, and concrete code snippets: full code for signatures, types, schemas, queries, and non-obvious logic; pseudocode only where the code is mechanical.
- Tests go under `## Tests`, one short bullet per behavior.

```md
## Architecture Overview

<Concise summary of the chosen architecture, how pieces fit together, and why this approach was chosen (drawing on repo conventions and any web research).>

## Steps

### 1. <short title>

In `<file path>`, <what this step does, mirroring sibling path>.

```ts
<concrete types, interfaces, signatures, or schemas>
```

### 2. <short title>

In `<file path>`, <implementation logic and handling>.

```ts
<concrete code snippet or query>
```

## Tests

- <short title for the one behavior this test proves>
```

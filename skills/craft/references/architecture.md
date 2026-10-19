## Standards

These standards bind everyone who designs, writes, reviews, or polishes code for this work. Follow the document shapes in `SKILL.md`; this reference covers design quality and review behavior.

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

### Architecture, steps, and tests

- In `architecture.md`, explain the chosen design, how its parts interact, why it fits the task and repo, and meaningful tradeoffs. Identify relevant paths, examples, and existing package or stdlib choices where useful. Keep implementation detail out of this design rationale.
- In `implementation.md`, describe concrete code changes in dependency order. Name real paths, symbols, existing patterns, approved contracts, and relevant error behavior. Include enough detail for a coder to build without guessing. Keep step status in `progress.md`.
- In `testing.md`, list observable checks and map each to one or more spec requirement IDs. Record automated results and live `Ran:` / `Saw:` evidence for every requirement.
- Keep the approved design, build steps, and test plan consistent; substantive changes reopen the architecture approval gate. Formatting and clarity edits that preserve approved meaning do not.

## Standards

These standards bind everyone who designs, writes, reviews, or polishes code for this work.

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

## Architecture, steps, and tests

Write the design in `.craft/<feature>/architecture.md`, build-ready work in `implementation.md`, and planned checks in `testing.md`. Start from [`../assets/templates/architecture.md`](../assets/templates/architecture.md), [`../assets/templates/implementation.md`](../assets/templates/implementation.md), and [`../assets/templates/testing.md`](../assets/templates/testing.md). Adapt the layout to the work; these are Markdown documents, not schemas.

1. **Architecture overview:** Explain the chosen design, how its parts interact, and why it fits the task and repo.
2. **Fit to the repo:** Identify relevant paths, examples to follow, and existing package or stdlib choices where useful.
3. **Build-ready steps:** Use numbered steps and substeps in dependency order to explain the implementation. Describe the concrete changes and how they work, choosing prose, code snippets, pseudocode, schemas, queries, or logic as appropriate. Include relevant edge and error behavior where it helps the coder build without guessing. Adapt the outline to the task rather than repeating fixed fields. Keep step status in `progress.md`.
4. **Test plan:** In `testing.md`, list specific observable behaviors to verify and map each check to one or more spec requirement IDs. Record automated check results and, after live testing, `Ran:` and concrete `Saw:` evidence for every requirement there.

Cover the chosen approach and its reasons. Include rejected alternatives only when they clarify an important tradeoff. Keep the approved design, build steps, and test plan consistent; changes to their substance reopen the architecture approval gate. Formatting and clarity edits that preserve approved meaning do not.

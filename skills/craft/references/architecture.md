# Architecture judgment

Apply when designing. Stay at system-design altitude — pieces, ownership, data flow, repo fit. Coding details, signatures, and pseudocode belong in the plan.

## Decompose first

Do not design the whole system as one blob. Break the problem down before choosing shapes:

1. **List the jobs.** What distinct responsibilities does this feature have? (persist X, expose Y, render Z, sync with W, …)
2. **Cut into independent components.** Keep splitting until each component owns one clear job and can be reasoned about alone. Two components are independent when either can change without forcing a rewrite of the other — they only meet at a narrow, named seam.
3. **Name the seams.** For each dependency between components, say what crosses it (data, events, calls) and which way it flows. No cycles: if A and B need each other, pull out the shared concept or merge them.
4. **Design each component, then the wiring.** Only after the cut is stable: how each piece fits the repo, what it hides, and how the seams connect. Prefer the simplest sound shape for each piece.
5. **Stop splitting when further cuts don't buy independence.** A small feature can be one component.

## Quality of a cut

- Group things that change together; split things that change for different reasons.
- Each component should hide one changeable decision behind a small interface. If you cannot name that decision, the cut is wrong. Never split by processing step or execution order alone.
- The deletion test: imagine deleting a component. If complexity vanishes, it was a pass-through; if it reappears across its callers, it earned its keep.
- The interface is the test surface: if a component must be tested past its interface, the cut is wrong.
- One implementation means a hypothetical seam — do not introduce an interface until a second real implementation exists.
- Prefer fewer deep components over many shallow ones.
- Keep dependencies one-way.
- Identify the 1–2 things most likely to change and contain them. Earn every new package, layer, or interface — only if you can name what it buys *today*.

## Quality bar

- Assume the team is highly particular about code quality and consistency.
- Prefer the least design that stays clear; no speculative generality, config knobs, or helpers without real duplication. Any deviation from the simplest shape must say why the simpler alternative was rejected.
- Prefer existing, well-maintained solutions over hand-rolling — modern stdlib, dependencies already in the project, or well-maintained third-party packages when appropriate. If unsure whether a good package exists, search the web.
- Stay inside the requested behavior; no drive-by refactors.
- Repo conventions beat personal preference. Mirror a nearby sibling feature before inventing structure.
- Verify unfamiliar APIs, symbols, and config against the repo or authoritative docs; never invent by analogy.

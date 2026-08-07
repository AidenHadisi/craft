# Principles

The [constitution](constitution.md) is binding. This file is design-time judgment — how to cut modules, shape code, and simplify — without restating its hard rules. Name the riskiest coupling and how your decomposition handles it.

## Architecture

### Repo fit

In an established codebase, reuse its package layout, layering, naming, and dependency direction. Do not introduce a new architectural style, folder scheme, or seam pattern unless the existing one is the proven source of pain — and say so explicitly. Before inventing structure, mirror a nearby sibling feature. A clean design that fights the house is wrong.

### Boundaries

A boundary is right when the things inside change together and the things across it change for different reasons.

- **Decision-hiding.** Name the one changeable decision a module hides. If you cannot, the boundary is wrong. Never split by processing step or execution order.
- **Deep modules.** Prefer a small, stable interface hiding substantial implementation. If the interface is as complex as what it hides, remove or move the boundary.
- **Shallow-component tax.** Many shallow components cost more total comprehension than fewer deep modules: interfaces multiply and working memory is limited.
- **Task cuts.** Split for coherent ownership, one-way dependencies, and parallel work — never for ceremony. "And" in a description is a signal to inspect, not an automatic split tax.
- **One-way coupling.** Name every cross-seam dependency and keep it one-way. No cycles: if A and B need each other, pull out the shared concept or merge them.

### Dependencies

- **Policy over mechanism.** Separate policy from I/O/persistence/framework types only when the repo already does so, or a real present seam justifies it; otherwise follow the house shape. When separated, mechanism depends on policy — never the reverse.
- **Interfaces at real seams.** Where the constitution permits an interface at a real external seam and it fits the repo, define the minimal shape where used; otherwise use the concrete type.
- **Domain seams.** Where two domains meet, translate explicitly — don't leak one model everywhere.

### Likely change & complexity budget

Identify the 1–2 things most likely to change, and contain each so a change touches one Task. Resist unasked flexibility. Earn every seam: add a component, layer, or interface only if you can name what it buys *today*. A small feature can be a single Task. Do not add layers the architecture didn't define.

## Code design

Prefer **readability > DRY > brevity**. Length alone is not a smell; mixed concerns and unclear flow are. Flatten and name steps locally before considering extraction. The constitution alone decides whether extraction is allowed; an allowed extraction must remove more complexity than it adds. Do not define constants for strings used once.

### Function shape

- **Linear flow; fewer, substantial functions.** Related logic that changes together stays together. Inline tiny helpers; locals name steps. One level of abstraction per body — don't mix wire parsing with business policy.
- A boolean flag hiding two behaviors wants two functions. Related parameters that travel together want a type.

### Naming

Intention-revealing: the name says what it is *for*, not what it is made of. Ban vague nouns (`Manager`, `Processor`, `Handler` outside transport, `Util`, `Helper`, `Data`, `Info`). One word per concept across the feature — pick `fetch` or `get` or `load` and stick with it.

### Errors

- **Errors are part of the contract.** Decide what callers can match on (sentinel, type, status) and document it where the contract lives.
- **Define errors out of existence.** Where contract semantics allow it, remove special cases (e.g. delete-missing as no-op) instead of stacking guards. Do not silently change established public contracts.

### State and data

Prefer immutable values; mutate only where required, in one owner. Make illegal states unrepresentable when cheap: parse into a typed value once at the boundary. Don't pass clusters of loose primitives — give the concept a type.

### Idioms

Precedence: **repo convention first**, canonical language/framework guide second, personal preference last. Prefer libraries the repo already depends on. Follow the repo's idioms even where you'd choose differently.

### Comments

Comments explain *why* — trade-offs, invariants, non-obvious contracts. A comment narrating the next line is noise; delete it.

## Refactoring

Scope any refactor to the feature's footprint. When planning, decide explicitly whether to refactor first as an early Task, or leave it with a stated reason.

### Simplification priority

1. Delete dead code
2. Inline function / variable (when the name isn't clearer than the body)
3. Inline class / collapse layer
4. Remove middle man
5. Drop unused / speculative parameters
6. When the constitution permits extraction, keep it only if the result is deep

### Smell → move

| Smell | Move |
| --- | --- |
| Helper wrapping obvious lines | Inline Function |
| Too many small functions for one flow | Inline into the few that do real work; locals name steps |
| Long function with unclear flow | Flatten locally first; Extract Function only where the constitution permits |
| Nested conditionals | Guard clauses / early return |
| Flag argument forking behavior | Two named functions |
| Layer that hides nothing / middle man | Collapse it |
| Two modules importing each other | Pull out shared concept, or merge |
| Speculative generality, dead code | Delete it |
| God object / shotgun surgery | Contain or split so change locality matches the decision |

## Self-critique

- **Over-built?** Every component, layer, seam, helper earning its place today? Cut and inline.
- **Under-built?** Missing boundary, unowned concern, missed edge, unhandled failure? Fix it.
- **Boundaries?** Decision named? Deep enough? One-way? Likely change local?
- **Names / readable?** Would a reader know each call without the body? Least code that stays clear.

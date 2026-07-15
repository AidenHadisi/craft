# Design Principles

The **code standard for the whole workflow** — followed when writing the plan, reviewing the plan, and polishing the implementation. The bar: code a strong senior engineer would merge without comment. Work through the sections in order — they cover how much code to write, how to shape it, name it, fail it, and when a pattern is justified.

## 1. Less code is better code

Every line must be read, understood, and maintained forever. The best design solves the problem in the fewest lines that remain clear. An abstraction must remove more complexity than it adds — otherwise discard it.

Never:
- Wrap 1–3 obvious lines in a helper. If the body is as simple as the call site, inline it.
- Add an interface with a single implementation — unless the architecture demands that seam.
- Write builders/factories that only set fields. Use literals.
- Extract single-use "validate"/"build"/"prepare" helpers. Keep the logic inline where it runs.
- Define constants for strings used once.
- Add layers the architecture didn't define (no service-wrapping-repository-wrapping-query).
- Extract a function because it is "long." Length alone is not a smell — mixed concerns and unclear flow are. Use local variables to name steps and early returns to flatten before reaching for extraction. Extract only to name a real concept, kill duplication across 3+ sites, or isolate a genuine responsibility.

## 2. Shape of a function

- **Linear flow.** Guard clauses and early returns; treat nesting depth as a defect.
- **Fewer, substantial functions.** Related logic that changes together stays together. A file full of 5-line helpers forces the reader to jump around — inline them into the 2–3 functions that do real work. Use local variables to name intermediate steps instead of extracting functions.
- **0–2 parameters.** Three related parameters want to be a type. A boolean flag hiding two behaviors wants to be two functions.
- **Command–query separation.** A function either does something or answers something, not both.
- **One level of abstraction per body.** Don't mix wire parsing with business policy in the same function.

## 3. Naming

- Intention-revealing: the name says what it is *for*, not what it is made of. A reader should not need the body to know what a call does.
- Ban vague nouns: `Manager`, `Processor`, `Handler` (outside transport layers), `Util`, `Helper`, `Data`, `Info`.
- One word per concept across the feature — pick `fetch` or `get` or `load` and stick with it.

## 4. Errors

- **Fail fast.** Validate at the boundary, return early, surface the failure where it happened.
- **Never swallow.** Every error is handled, propagated with context, or crashes loudly. A logged-and-ignored error is a swallowed error.
- **Errors are part of the contract.** Decide what callers can match on (sentinel, type, status) and document it where the contract lives.

## 5. State and data

- Prefer immutable values; mutate only where the design requires it, in one owner.
- Make illegal states unrepresentable when it's cheap: parse input into a typed value once at the boundary instead of re-validating raw primitives everywhere downstream.
- Don't pass clusters of loose primitives around (primitive obsession) — give the concept a type.

## 6. Patterns earn their place

Use a design pattern only when it removes real, present complexity. Name the simpler alternative you rejected — it is usually a plain function.

| Pattern | Justified when | Default to instead |
|---|---|---|
| Strategy | 3+ interchangeable behaviors selected at runtime | a function parameter |
| Factory | construction needs real branching or invariants | a literal or constructor |
| Decorator | optional behavior layered over a stable interface | a wrapping function |
| Observer / pub-sub | many decoupled reactions to one event | a direct call |
| Adapter | a foreign interface must fit a local seam | using the type directly |
| Template method | fixed skeleton with varying steps | composition with functions |

While designing, also watch for the classic smells: duplicated logic, feature envy, shotgun surgery, leaky abstraction.

## 7. Modern and idiomatic

- Check the target version (`go.mod`, `tsconfig`, `pyproject.toml`, …) and use the modern primitives it provides before writing custom ones.
- Prefer well-maintained libraries over hand-rolled utilities — never reinvent dates, retries, validation, parsing, or serialization. Prefer libraries the repo already depends on over new ones.
- Follow the repo's idioms — error style, import grouping, test layout, naming — even where you'd personally choose differently. Idiomatic-for-the-language that fights the house is still wrong.

## 8. Testable by design

Make the architecture's boundaries real seams in code: inject dependencies exactly where the architecture defined a seam (and nowhere else), and keep pure logic free of I/O so it can be tested without mocks.

## 9. Comments

Comments explain *why* — trade-offs, invariants, non-obvious contracts. A comment narrating the next line is noise; delete it.

## 10. Refactoring moves

Smell → move. One line each — use these names when fixing or polishing.

| Smell | Move |
|---|---|
| Helper wrapping 1–5 obvious lines | Inline Function — the single most common defect; hunt actively |
| Too many small functions for one flow | Inline into the 2–3 functions that do real work; local variables name steps |
| Long function with unclear flow | Local variables + early returns first; Extract Function only for a real concept or 3+ duplication |
| Nested conditionals | Guard Clauses / early return |
| Unreadable boolean | Extract Variable — name the condition |
| Long parameter list / data clump | Introduce Parameter Object |
| Flag argument forking behavior | Remove Flag Argument — two named functions |
| Function envying another module's data | Move Function to where the data lives |
| Magic literal | Named constant (2+ uses) or inline with a comment |
| Temp reused for different purposes | Split Variable |
| Loop doing several jobs | Split Loop; Replace Loop with Pipeline |
| Primitive obsession | Introduce a type — enum, value object, or wrapper |
| Repeated switches on the same discriminant | Polymorphism or one shared lookup map |
| Duplicated logic (3+ sites) | Extract Function — one definition, right home |
| Speculative generality, dead code | Delete it |

## Self-Critique

Argue against the design before finishing:

- **Over-built?** Tiny helpers, single-implementation interfaces, patterns without payoff? Cut and inline.
- **Under-built?** Missed edge cases, unhandled failures, swallowed errors? Fix them.
- **Boundaries honored?** Does the code respect the architecture's seams?
- **Names carry meaning?** Would a reader know what each call does without the body?
- **Readable and concise?** Least code that stays clear — no nesting pyramids, no 60 lines where 20 do.

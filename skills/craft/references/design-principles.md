# Design Principles

Read this before designing a Task's implementation (Phase 9). Apply these principles directly and tie every choice to the code you write.

## Less Code is Better Code

Every line is a line to be read and maintained. The best design solves problems in the fewest lines while remaining readable. Abstractions should reduce total complexity—if they add code without removing confusion, discard them.

**Do not:**
- Wrap 1–3 obvious lines in a helper.
- Create builder/factory functions just to set struct fields—use literals.
- Add interfaces unless there are multiple implementations or strict test requirements.
- Extract a single-use "validate" helper—keep the checks inline.
- Define constants for single-use strings.
- Add extra layers (e.g., service, repository) beyond what the architecture defines.
- Extract a function merely because it is "long." Only extract to name a real concept, remove duplication across 3+ sites, or isolate a genuine responsibility.

## Readable and Clean

- **Keep it linear:** Prefer a simple linear flow with early returns over deep nesting.
- **Be expressive:** Use intention-revealing names.
- **Minimize arguments:** Aim for 0–2 arguments. Avoid boolean flags that hide two behaviors in one function.
- **Fail fast:** Validate inputs early. Never swallow errors.
- **Comment the *why*:** Comments should explain reasoning, not narrate the code.

## Patterns Earn Their Place

Use design patterns only when they eliminate real, present complexity. Name the simpler alternative you rejected (often a plain function). Avoid primitive obsession, feature envy, duplicated code, shotgun surgery, and leaky abstractions.

## Modern and Idiomatic

Prefer well-maintained libraries over hand-rolled utilities. Use the latest stable language features. Follow the repository's existing idioms and import styles. Keep it DRY, but never sacrifice clarity.

## Testable

Make the architecture's boundaries real seams in code. Inject dependencies where dictated by the architecture, and keep pure logic easily separable.

## Task Body Template

Add this content under the existing `### Task K — <component>` header in your plan:

1. **Design Note:** 2–4 sentences detailing the units (files/functions) added, the **concrete public contract exposed**, the key pattern chosen, and the rejected alternative.
2. **Subtasks:** Ordered sequentially (`#### Subtask K.1`, `K.2`, etc.). Each must include:
   - The target **file path** and action (`· create` or `· edit`).
   - A fenced block of **complete literal code**, OR
   - A **manual action** (e.g., DDL, migration, install) tagged with `· manual` so coders skip it.
   *Ensure each subtask compiles on top of the previous ones.*

> **Note:** The public contract you expose serves as the foundation for downstream Tasks. Make it explicit and stable.

## Self-Critique

Argue against your design before presenting it:

- **Over-built?** Are there tiny helpers, single-implementation interfaces, or unnecessary patterns? Cut them. Inline where possible.
- **Under-built?** Did you miss edge cases, unhandled failures, or swallowed errors? Fix them.
- **Boundaries honored?** Does it strictly respect the architecture's seams and upstream contracts?
- **Contract stable?** Is the exposed API explicit enough for downstream Tasks?
- **Zero decisions left?** Could a coder implement it verbatim without inventing anything?

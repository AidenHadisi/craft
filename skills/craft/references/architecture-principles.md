# Architecture Principles

Read this before decomposing a feature into Tasks (Phase 7). Apply these principles directly to your system—state the riskiest coupling and how your decomposition mitigates it.

## Principles

### Boundaries & Decomposition
- **Cut at Concept Boundaries:** Separate concerns that change for different reasons. Each component must own exactly one responsibility.
- **Design Deep Components:** Expose a small, stable interface that hides substantial implementation complexity. Reject interfaces that are as complex as what they hide.
- **Maximize Cohesion, Minimize Coupling:** Name dependencies across seams and keep them **one-way**.
- **Dependency Rule:** Source-code dependencies should point inward toward policy. Mechanism (I/O, persistence, frameworks) depends on policy, never the reverse.
- **Watch Component Health:** Prevent dependency cycles. The more stable a component, the more abstract it should be.
- **Bounded Contexts:** Where domains meet, define a bounded context with explicit translation rather than leaking a single model everywhere.

### Architectural Style
- **Keep It Simple:** Pick the simplest style that fits (e.g., layered, ports-and-adapters). The style is a means to achieve clean boundaries, not an end in itself.

### Designing for Change
- **Evolutionary Architecture:** Identify the most likely areas of change and isolate them. A simple, replaceable structure is better than over-generalized speculation.
- **Resist Unasked Flexibility:** Only absorb plausible changes. Unnecessary flexibility is a defect.

### Complexity Budget (YAGNI)
- **Earn Every Seam:** Add a component, layer, or seam only if it pays for itself immediately. If you can't name what a boundary buys today, remove it.
- **Don't Over-decompose:** A small feature can be a single Task. Do not force splits.

### Refactoring Lens
- **Fix Structural Smells:** When touching existing code, note smells (e.g., leaky abstractions, god objects). Explicitly decide whether to refactor first or leave it with a stated reason. Scope refactors strictly to the feature's footprint.

## Plan Template

Use this structure for `docs/plans/<feature>.md`. Keep architecture at the component level. **No signatures, types, file lists, or schemas here** (add those in Phase 9).

```markdown
## Architecture & design

### Overview
2–4 sentences describing the shape of the solution, the architectural style, and why it fits.

### Tasks (units)
One row per Task representing feature components:

| Task | Component | Responsibility | Owns (area) | Depends on | Exposes (capability) |
|---|---|---|---|---|---|
| 1 | <name> | One-line summary | `target/package` | — or Task N | Capability offered |

### Boundaries & data flow
Describe dependency direction (one-way) and data paths. Include a Mermaid diagram. **No signatures.**

### Design decisions
Document notable choices: decision, reasoning, and rejected alternatives.

## Tasks

### Task 1 — <component>   (depends on: none · exposes: <capability>)

### Task 2 — <component>   (depends on: Task 1 · exposes: <capability>)

## Verification
A one-liner detailing what "done" means (e.g., build/typecheck/tests/manual checks).
```

## Self-Critique

Argue against your own decomposition before presenting it:

- **Over-built?** Does every component, layer, or seam earn its place? If not, cut it.
- **Under-built?** Are there missing boundaries, unowned concerns, or vague seams? Fix them.
- **Cyclic dependency?** Are there two-way couplings between Tasks? Break them.
- **Wrong granularity?** Should two Tasks be merged, or one split?

Defend every boundary by its cohesion, one-way coupling, and locality of change.

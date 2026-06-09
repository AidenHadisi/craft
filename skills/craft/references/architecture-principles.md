# Architecture Principles

How to decompose a feature into Tasks (Phase 7). Work through the sections in order — they mirror the decisions you actually make: where to cut, which way dependencies point, what style to use, what change to absorb, and what complexity to refuse. Never name a principle without a concrete claim about *this* design: state the riskiest coupling and how your decomposition handles it.

## 1. Cut at concept boundaries

A boundary is right when the things inside change together and the things across it change for different reasons.

- **One responsibility per component.** Each Task owns exactly one concern. If describing it needs "and", it's two Tasks.
- **Design deep modules.** A small, stable interface hiding substantial implementation. If the interface is as complex as what it hides, the boundary buys nothing — remove it or move it.
- **Maximize cohesion, minimize coupling.** Name every dependency that crosses a seam, and keep each one one-way.

## 2. Point dependencies inward

- **Policy over mechanism.** Business rules never import I/O, persistence, or framework types. Mechanism depends on policy, never the reverse.
- **No cycles.** If Task A and Task B need each other, the cut is wrong — extract the shared concept, or merge them.
- **Consumers own their abstractions.** Define an interface where it is used, not where it is implemented (the handler declares the store interface it needs; the store just satisfies it).
- **Translate at domain seams.** Where two domains meet, define a bounded context with explicit translation instead of leaking one model everywhere.

## 3. Pick the simplest style that fits

The style is a means to clean boundaries, not an end. Match the repo's existing style unless it is the proven source of pain.

| Shape of the problem | Reach for |
|---|---|
| CRUD over a domain, one direction of flow | Layered: handler → domain → store |
| Core logic must outlive its I/O (swappable DB, API, queue) | Ports & adapters |
| Data moves through ordered transformations | Pipeline of pure steps |
| Many independent reactions to one event | Pub/sub — only if the decoupling pays today |

## 4. Design for likely change, not imagined change

- Identify the 1–2 things most likely to change in this area, and contain each so a change touches one Task.
- **Resist unasked flexibility.** Config hooks, plugin points, and generality nobody requested are defects, not foresight. A simple, replaceable structure beats a speculative general one.

## 5. Spend the complexity budget honestly

- **Earn every seam.** Add a component, layer, or interface only if you can name what it buys *today*. If you can't, cut it.
- **Don't over-decompose.** A small feature can be a single Task. Never force splits to look thorough.

## 6. Refactor lens (existing code only)

When the feature touches existing code, weigh the smells the explorers reported (god object, leaky abstraction, duplicated logic, shotgun surgery). Decide explicitly: refactor first as an early Task, or leave it with a stated reason. Scope any refactor strictly to the feature's footprint.

## Plan Template

Use this structure for `docs/plans/<feature>.md`. Keep the architecture at the component level — **no signatures, types, file lists, or schemas yet** (those come in Phase 9).

```markdown
## Architecture & design

### Overview
2–4 sentences: the shape of the solution, the architectural style, and why it fits this problem and this repo.

### Tasks (units)
One row per Task:

| Task | Component | Responsibility | Owns (area) | Depends on | Exposes (capability) |
|---|---|---|---|---|---|
| 1 | <name> | One-line summary | `target/package` | — or Task N | Capability offered |

### Boundaries & data flow
Dependency direction (one-way) and data paths, with a Mermaid diagram. **No signatures.**

### Design decisions
Each notable choice: the decision, the reasoning, and the rejected alternative.

## Tasks

Order Tasks so each compiles on top of the ones before it. If Task 2 uses anything from Task 1, Task 1 comes first.

### Task 1 — <component>   (depends on: none · exposes: <capability>)

### Task 2 — <component>   (depends on: Task 1 · exposes: <capability>)

## Verification
What "done" means: build/typecheck/lint/tests/manual checks.
```

## Self-Critique

Argue against your own decomposition before presenting it:

- **Over-built?** Does every component, layer, and seam earn its place today? If not, cut it.
- **Under-built?** Any missing boundary, unowned concern, or vague seam? Fix it.
- **Cyclic?** Any two-way coupling between Tasks? Break it.
- **Wrong granularity?** Should two Tasks merge, or one split?
- **Wrong style?** Would a simpler style produce the same boundaries with less machinery?

Defend every boundary by its cohesion, its one-way coupling, and the locality of likely change.

# Architecture Principles

The **structural standard for the whole workflow** — followed when decomposing the plan, judging a design review, and restructuring a working diff. Work through the sections in order — they mirror the decisions you actually make: where to cut, which way dependencies point, what style to use, what change to absorb, and what complexity to refuse. Never name a principle without a concrete claim about *this* design: state the riskiest coupling and how your decomposition handles it.

**Repo fit first.** In an established codebase, reuse its package layout, layering, naming, and dependency direction. Do not introduce a new architectural style, folder scheme, or seam pattern unless the existing one is the proven source of pain — and say so explicitly. A clean design that fights the house is wrong. Before inventing structure, mirror a nearby sibling feature in the same area.

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

The style is a means to clean boundaries, not an end. **Fit the repo first** — the table below is a fallback when the area has no established pattern, not a license to replace one that works.

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

## 6. Refactor lens

Weigh structural smells in code the feature touches or produces (god object, leaky abstraction, duplicated logic, shotgun surgery, wrong home for a concept). When planning: decide explicitly whether to refactor first as an early Task, or leave it with a stated reason. When polishing or reviewing: apply the moves below. Scope any refactor strictly to the feature's footprint.

| Smell | Move |
|---|---|
| Function/type living away from its data | Move it to where the data lives |
| Layer that hides nothing (interface as complex as what it wraps) | Collapse the layer |
| Two modules importing each other | Extract the shared concept, or merge them |
| Module serving two masters ("and" in its responsibility) | Split at the concept boundary |

## Self-Critique

Argue against your own decomposition before presenting it:

- **Over-built?** Does every component, layer, and seam earn its place today? If not, cut it.
- **Under-built?** Any missing boundary, unowned concern, or vague seam? Fix it.
- **Cyclic?** Any two-way coupling between Tasks? Break it.
- **Wrong granularity?** Should two Tasks merge, or one split?
- **Wrong style?** Would a simpler style produce the same boundaries with less machinery?

Defend every boundary by its cohesion, its one-way coupling, and the locality of likely change.

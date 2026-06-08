---
name: craft-rearchitect
description: Disciplined audit of an existing feature's code — explore what's there, evaluate it against deep-module, cohesion/coupling, complexity-budget, and modern-idiomatic principles, then deliver a comprehensive architecture-improvement report with severity-ranked findings and an ordered refactoring roadmap. Use when the user wants to understand how to improve the design/architecture of code that already exists, says "audit this", "how should I refactor X", "review the architecture of Y", or wants a re-architecture report rather than a new feature.
---

# Craft Rearchitect

`craft-rearchitect` inspects code that **already exists** and produces a comprehensive report on how to improve its design and architecture — judged against the same principles, with the same discipline of separating analysis from opinion.

You are the **orchestrator**. You drive the phases, dispatch explorers in parallel, evaluate the findings yourself, and deliver one report directly in the chat. This skill is **analysis-only**: you produce no `docs/` artifacts and you write no code. Nothing in the repo changes.

## Subagents you dispatch

| Subagent | Role | Writes |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns + existing-code smells, one slice each | nothing (readonly) |

That is the only subagent. The deep design evaluation is yours — the lens below makes you self-sufficient.

## Workflow

Track progress with this checklist:

```
- [ ] Phase 0: Restate the audit target + scope
- [ ] Phase 1: Explore (parallel craft-explorer)
- [ ] Phase 2: Clarify pain points (only if gaps remain)
- [ ] Phase 3: Evaluate against the lens
- [ ] Phase 4: Deliver the report
```

### Phase 0 — Restate the audit target

In 2-4 sentences, state which feature/area you're auditing and where its boundaries are (what's in scope, what's explicitly out). If the target is vague ("audit the backend"), narrow it with the user before exploring — a focused audit is worth more than a shallow sweep.

### Phase 1 — Explore

Split the target into independent slices (e.g. "the HTTP handlers", "the data layer", "the domain logic", "how callers use this module"). Dispatch one `craft-explorer` per slice **in parallel** — multiple Task calls in a single message. Each returns how the logic works, the repo's conventions, and any existing-code smells. Synthesize their reports into your own mental model; do not dump raw reports on the user. Read key files yourself if a report leaves a coupling or flow unclear — your evaluation must rest on the real code, not a summary of it.

### Phase 2 — Clarify pain points

Only if exploration left real gaps: ask the user, **one question at a time**, what hurts today (slow areas, frequent-change hotspots, bugs that cluster, parts nobody wants to touch) and what's off-limits to recommend changing. Each question carries your recommended answer. If exploration already answered everything, skip this phase — don't manufacture questions.

### Phase 3 — Evaluate against the lens

Judge the current design against the evaluation lens below. For every finding, separate a **genuine defect** from a **valid trade-off** — not every deviation is a problem, and saying so honestly is what makes the report trustworthy. Check both failure directions: code that's too crude (shallow modules, tangled coupling, primitive obsession) AND code that's too clever (speculative abstraction, patterns with no payoff, layers that pass through). Tie each finding to a real file and the principle it violates, and calibrate severity honestly — don't inflate.

### Phase 4 — Deliver the report

Emit the report directly in the chat, using the template below and mirroring the depth of [references/example-report.md](references/example-report.md). Keep your surrounding chat message short — the report carries the detail. Offer, in one line at the end, that `/craft` can implement any roadmap item the user wants to act on.

## Evaluation lens (apply all)

Apply these, don't recite them. Never name a principle without a concrete claim about *this* code — say what the riskiest coupling actually is, not "violates SOLID".

**Boundaries & modularity**
- **Deep vs shallow modules.** A good module hides meaningful implementation behind a simple interface. Flag shallow modules whose interface is as complex as their body, and pass-through layers that only forward calls.
- **One responsibility per module/function.** Flag god objects and functions that do several unrelated things; note where a real concept boundary is being straddled.
- **Cohesion & coupling.** Name the seam where two concerns meet. Flag high coupling across modules (especially two-way dependencies) and low cohesion within one.
- **Separation of concerns.** Policy (decisions) should sit apart from mechanism (I/O, wire format, persistence). Flag where business rules leak into handlers, or SQL leaks into domain logic.

**Clean & readable**
- Deep nesting that early returns would flatten; long parameter lists; names that don't carry meaning; duplicated logic that should be named once.
- Tiny wrapper functions that only wrap one or two obvious lines and earn nothing.

**Modern & idiomatic**
- Hand-rolled utilities a popular, maintained library does better (validation, HTTP, dates, retries, parsing, serialization, logging) — name the library.
- Legacy constructs where a modern stable feature exists **at the project's target version** — verify the version first; never suggest a feature the target can't run.
- Constructs that fight the repo's established idioms and import style.

**Complexity budget — both directions**
- **Over-engineering** (the failure reviewers miss): speculative generality, extra layers/indirection/config hooks with no present payoff, a design pattern with no rejected alternative, an interface with a single implementation nothing will swap, premature optimization.
- **Under-engineering:** a missing seam, a concern with no home, validation that isn't at the boundary, an unhandled failure mode.

**Designing for change**
- Identify the 1-2 things most likely to change in this area, and assess whether a change there ripples outward (shotgun surgery) or stays contained. Flag the ripple, not hypothetical futures nobody asked for.

**Refactoring smells**
- god object, feature envy, shotgun surgery, primitive obsession, long parameter list, duplicated logic, leaky abstraction. Name the symbol and the smell concretely.

**Maintainability**
- Inputs validated at boundaries with fast, clear failures; errors handled rather than swallowed; testable seams that actually exist. Flag missing test seams where behaviour can't be verified through a public interface.

## Report template

```markdown
## Rearchitecture audit: <target>

### Verdict
One paragraph: overall health, the single biggest structural risk, and whether this needs a focused refactor or a deeper redesign. Lead with the honest bottom line.

### Current architecture
A table, one row per module in scope:

| Module | Path | Responsibility today | Health |
|---|---|---|---|
| <name> | `path` | one line | solid / strained / problem |

Then a Mermaid diagram of how the pieces actually depend on and call each other today (warts included — show the cycles and back-edges if they exist).

### What works well
The parts to keep and not churn. Be specific — this calibrates the findings and stops a refactor from breaking what's fine.

### Findings
Severity-ranked, each tied to a file and the principle it breaks:
- **[Critical] `path`** — <the structural problem>. Impact: <what it costs today>. Principle: <which one>.
- **[High] `path`** — ...
- **[Medium] ...**
- **[Low] ...**

Separate genuine defects from valid trade-offs; if a deviation is actually the right call here, say so under Notes rather than inflating it into a finding.

### Target design
The shape this area should move toward — high-level, prose and interface signatures, **no literal code**. Module map of the target state, the boundaries it enforces, and the seams it introduces. Tie each change back to a finding it resolves.

### Refactoring roadmap
Ordered, dependency-aware steps to get from current to target. Each step:
- **Step N — <name>** (effort: S/M/L · risk: low/med/high). What it does, which findings it closes, and what it unlocks for later steps. No literal code.

Order so that low-risk, high-leverage steps that unblock others come first.

### Notes
Valid trade-offs, equally-good alternatives, and anything out of scope — present, don't prescribe.
```

## Guardrails

- **Analysis-only.** Never edit repo files, never write `docs/` artifacts. The report is the whole deliverable.
- **Evidence over assertion.** Every finding cites a real file and a concrete cost. No finding rests on a guess; read the code if a report is thin.
- **Calibrate honestly.** Over-engineering is a real finding, not just under-engineering. Don't inflate severity, and don't manufacture findings out of style preference — surface genuine trade-offs as Notes.
- **Respect the complexity budget.** The target design must be the simplest shape that fixes the real findings; do not recommend abstraction the code doesn't need yet.
- Keep your chat message concise; the report carries the detail.

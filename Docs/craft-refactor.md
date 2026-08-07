# craft-refactor — Deep Refactor Skill Design

Research and design document for a new craft skill that performs deep, multi-agent refactoring toward smaller, lower-cognitive-load code. It is the thorough evolution of the `craft-polisher` subagent: where the polisher does a single-pass cleanup of a working diff, this skill decomposes a target, redesigns its components with fresh-context subagents, wires them back together, and rewrites — with a user approval gate before any code changes.

## The problem

AI coding agents produce over-verbose, over-engineered code: unnecessary few-line helpers, speculative validation and guardrails, future-proofing nobody asked for, generic names, and module boundaries chosen by accident of generation order rather than design. This is measured, not anecdotal:

- Agent-written code is **~2.2× more verbose** than comparable human repos, and verbosity **rises in ~90% of iterative trajectories** — meaning the problem compounds as agents extend their own code, and one-time prompt instructions do not stop the decay ([SlopCodeBench, 2026](https://arxiv.org/html/2603.24755v1)). Recurring, dedicated redesign passes are required.
- Models systematically avoid deleting: they make only **¼–⅓ of the deletions** humans would, preferring to wrap old code rather than remove it ([To Add Is Machine, To Delete Is Human](https://arxiv.org/html/2607.28887)).
- **19–35% of LLM "behavior-preserving" refactors actually change semantics**, and ~21% of those still pass the existing test suite ([differential testing studies](https://arxiv.org/html/2602.15761)) — so tests alone are not a sufficient safety net for a rewrite skill.
- LLM judges have a **measured bias toward longer code** — a reviewer agent asked "is this good?" favors the verbose version ([TRACE](https://arxiv.org/html/2603.24586v2)). Review rubrics must explicitly reward deletion and penalize length.

## Key decisions

| Decision | Choice |
|---|---|
| Scope | Flexible — user points it at a diff, module, package, or repo |
| Behavior | Preserving by default; contract-changing improvements are flagged for approval, never applied silently |
| Autonomy | Approval checkpoint: full redesign presented before any rewrite (like craft's plan approval) |
| Competing designs | Best-of-N (2–3 designers, smallest-green selection) only for components the skill judges high-stakes |
| Verification | Parse → lint/types → existing tests; flag when coverage looks too weak to trust the rewrite |
| Principles | Reuse craft's shared standards, substantially upgraded (see "Shared reference foundation") |

## Intellectual foundation

### Decompose by decisions, not by size

The user-visible framing "split the system into smallest logical components" is the one part of the original idea the literature corrects. [Parnas (1972)](https://doi.org/10.1145/361598.361623) showed experts decompose by asking **"what design decisions are likely to change, and which module hides each one?"** — never by processing steps or by making pieces small. [Ousterhout](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) extends this: complexity = dependencies + obscurity, and the goal is **deep modules** — small stable interfaces hiding substantial implementation. Many tiny components each designed "cleanly" in isolation produce *higher* total cognitive load than fewer, deeper modules (interfaces multiply; working memory holds only ~4 chunks — [Cowan 2001](https://memory.psych.missouri.edu/assets/doc/articles/2001/cowan-bbs-2001.pdf), operationalized for code in [Cognitive load is what matters](https://zakirullin.md/cognitive)).

So the skill's decomposition step finds the **few deep boundaries**, and a small target may legitimately be a single component.

### Simplification has a canonical move order

From [Fowler's Refactoring (2nd ed)](https://martinfowler.com/articles/refactoring-2nd-changes.html), the moves that matter for simplification specifically, in priority order:

1. Remove Dead Code
2. Inline Function / Inline Variable (when the name isn't clearer than the body)
3. Inline Class / Collapse Hierarchy
4. Remove Middle Man
5. Change Function Declaration (drop unused/speculative parameters)
6. Extract — only when the constitution permits it, and only when the result is deep in Ousterhout's sense (simple interface hiding real complexity), never to hit a length quota

Delete before inline, inline before collapse, extract last. The shared `principles.md` records this order alongside its smell-indexed refactoring table.

Supporting doctrine, each with an operational rule the skill encodes:
- [Semantic compression](https://caseymuratori.com/blog_0015) (Muratori): write concrete code before abstracting. Muratori proposes the second occurrence; craft waits for duplication at 3+ sites before sharing a helper, while a genuine responsibility may justify a deep module earlier.
- [Carmack's inlining email](https://cbarrete.com/carmack.html): inline single-caller impure helpers; keep purity boundaries explicit.
- [YAGNI](https://martinfowler.com/bliki/Yagni.html) (Fowler): unused extensibility isn't just waste, it actively obstructs; delete hooks whose only clients are imaginary futures.
- [Define errors out of existence](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) (Ousterhout): redesign API semantics so exceptional cases aren't exceptional, instead of stacking guards.

### Success is multi-signal, never LOC alone

Static metrics individually predict maintainability weakly. The skill scores a refactor on the combination: net LOC down, cognitive complexity down ([SonarSource whitepaper](https://www.sonarsource.com/docs/CognitiveComplexity.pdf) — note it's gameable by scattering logic into shallow helpers, which is exactly the defect being fought, so it's paired with hop-count/module-count signals), cross-module dependencies down, public surface down, dead/speculative code gone. Raw LOC targets are dangerous: on hard tasks models collapse into garbage or delete necessary code to hit them ([Where Do LLMs Fail](https://arxiv.org/html/2406.08731v2)).

## What steers LLMs toward simpler code — ranked by evidence

1. **Terse behavioral constitutions.** ~10 hard MUST/NEVER rules, loaded early, beat long style guides. "Minimal code that works" directives measured a **56–70% token reduction with no correctness loss** ([Show and Tell](https://arxiv.org/abs/2511.13972)). Compliance decays sharply with rule count — ~68% at 500 instructions ([IFScale](https://arxiv.org/html/2507.11538)); one practitioner measured 94.8% vs 86.6% compliance for terse vs verbose phrasing ([Harness Engineering](https://blog.vtemian.com/post/harness-engineering/)). Implication: keep principle files short and load them per-pass, not as one dump.
2. **Fresh-context redesign agents.** The generation context contains the sunk-cost justification for every unnecessary helper; a blank-context agent seeing only code + contract has no attachment to them. Anthropic's production systems verify in separate contexts from the writer ([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). No controlled A/B on simplicity metrics exists yet, but the mechanism is the strongest architectural match to the failure mode.
3. **Anti-verbosity rubrics for judges.** Because judges prefer longer code, the critic's rubric must explicitly reward deletion, penalize length, require quoted line evidence, and issue PASS/REVISE verdicts rather than 1–10 scores.
4. **Explicit deletion targets.** Counter deletion-avoidance by making every design enumerate what gets deleted, and scoring net removals in the report.
5. **Best-of-N with smallest-green selection.** Competing redesigns help only if selection picks the **smallest passing** candidate; majority voting reinforces popular verbose patterns ([ensemble studies](https://arxiv.org/abs/2510.21513v2)).
6. **Structure pass before surface pass.** Never chase line count in the same pass that decides architecture — validated by practitioner consensus and already the polisher's ordering.

## Prior art worth stealing from

| Mechanism | Source |
|---|---|
| Decompose → present plan → **user approval** → isolated worktree agents → per-unit verification | [Claude Code `/batch`](https://code.claude.com/docs/en/commands) |
| Four parallel review lenses over one diff (reuse, simplification, efficiency, abstraction level) | [Claude Code `/simplify`](https://code.claude.com/docs/en/commands) |
| Adversarial verification — a *different* agent tries to refute each result; tournament selection | [Anthropic dynamic workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) |
| Bounded waves: fan-out → aggregate → verify evidence → extend only if gaps warrant; stop on stagnation/budget | [WAVES skill](https://github.com/RayFernando1337/rayfernando-skills) |
| Fresh implementer per task + reviewer who reads the code, never trusts the implementer's summary | [Superpowers subagent-driven development](https://github.com/obra/superpowers) |
| Deterministic transforms first, LLM only for judgment residue; shard landing by ownership | [Codemod workflows](https://docs.codemod.com/workflows/introduction), [Moderne](https://www.moderne.io/blog/ai-assisted-refactoring-in-the-moderne-platform) |
| Anti-laziness structural checks (AST node counts) to catch elided code | [Aider refactor benchmark](https://aider.chat/docs/leaderboards/refactor.html) |

The consensus: production systems never let one smart agent rewrite a module in place. They decompose, isolate, gate on approval, and verify with a different context than the writer.

## Skill design

New skill `skills/craft-refactor/SKILL.md`, following craft's existing orchestrator conventions (structured subagent briefs, parallel dispatch, main agent writes all shared artifacts).

### Phase 1 — Map

Dispatch generic parallel subagents over the target, each with a focused prompt and output contract for one slice or question. Assign the change-axis findings to the relevant slices rather than one universal report — what varies together, cross-module dependencies, public surface, duplicated logic, hotspots (high-churn files via `git log`), and an inventory of suspected over-engineering (single-use helpers, abstraction-theater interfaces beside their only implementation — a minimal consumer-owned interface at a real external seam is allowed when needed — speculative parameters, dead branches). Also gather conventions and how the logic works where those slices need them.

### Phase 2 — Cut

The main agent proposes component boundaries **by decision-hiding**: each component owns one changeable decision, has a small interface relative to what it hides, and no cycles. Explicitly resist over-decomposition — a small target is one component. Rejected cuts are noted with reasons (this becomes part of the checkpoint presentation).

### Phase 3 — Design in parallel

One fresh-context designer subagent per component. Each brief contains only: the component's current code, its contract (callers, tests, wire formats), the relevant principle files, and the constitution. No generation history. Each returns:

- Proposed design (interfaces first, comment-first style)
- **Deletion list** — named functions/types/branches to remove
- **"Deliberately not added"** — what was considered and rejected
- Flags — contract changes, new dependencies, anything outside its footprint

For components the orchestrator judges high-stakes (core domain logic, wide blast radius, gnarly current state), dispatch 2–3 competing designers and select the smallest design that satisfies the contract.

### Phase 4 — Wire

The main agent (this is the judgment step that shouldn't be delegated) produces the connection plan as a first-class artifact: shared types, call graph, which seams between components collapse entirely, migration order. This is where "how do these modules better connect so we write less code" is decided — often the biggest wins are boundaries that dissolve.

### Phase 5 — Adversarial review

A fresh critic subagent attacks the combined design with the anti-verbosity rubric: quoted-evidence findings, severity-tagged, PASS/REVISE verdict. Questions include "would a staff engineer delete this?", "is any interface as complex as what it hides?", "does any component exist to look thorough?". Revise until pass.

### Phase 6 — Checkpoint

Present to the user: component map with before/after sketch, the full deletion list, expected signal deltas, flagged contract changes (each needing explicit approval), and rejected alternatives. **No file is edited before approval.**

### Phase 7 — Rewrite in waves

Craft-coder subagents execute per component in dependency order (independent components in parallel). Two passes per component, never merged: **structure** (moves, merges, collapses, deletions per the design) then **surface** (names, idiom, modernity — per the polisher's Surface pass). After each wave, the verification ladder: parse → lint/types → existing tests. If test coverage over a rewritten area looks too weak to catch semantic drift, flag it prominently rather than claiming safety. Failed verification gets a capped retry budget (2), then escalates to the user.

### Phase 8 — Report

Net LOC delta, helpers inlined, layers collapsed, deletions executed vs planned, signals moved, flags not done. An honest "the design was already right, nothing to do" is a valid outcome at any phase.

## Shared reference foundation

The research is implemented through three plugin-root standards split by load scenario:

1. **`standards/constitution.md`** — the short MUST/NEVER writing rules and anti-verbosity diff rubric, loaded first by every writer and judge.
2. **`standards/principles.md`** — architecture, code-design, and refactoring judgment, including decision hiding and the simplification order. Deletion targets and "Deleted / Deliberately not added" reporting live in the constitution.
3. **`standards/testing.md`** — test-selection and mocking guidance, loaded when planning, writing, or reviewing tests.

The coder, code reviewer, plan reviewer, polisher, and orchestrator point to these shared files instead of restating the rules. Keeping each file aligned to one scenario reduces instruction dilution while giving every rule one maintained home.

## Known failure modes and their mitigations

| Failure mode | Mitigation in this design |
|---|---|
| Semantic drift passing weak tests | Coverage-weakness flag; behavior-preservation is checked by a fresh critic reading the diff, not the writer |
| Over-deletion (stripping needed code/comments to look minimal) | Principles keep non-obvious *why* comments; tests are a hard constraint; deletion list is pre-approved, not improvised |
| Judge rubber-stamping verbose designs | Anti-verbosity rubric with quoted evidence |
| Shallow-helper gaming of complexity metrics | Multi-signal scoring; principles require fewer, deeper modules |
| Infinite polish loops | Bounded waves, capped retries, "empty refactor is a valid outcome" |
| Over-decomposition to look thorough | Decision-hiding test per boundary; single-component targets allowed |

## Open questions

- Whether Phase 1 should compute cognitive-complexity scores mechanically (via lizard/SonarLint-style tooling when available) or rely on subagent judgment. Start with judgment; add tooling if reports feel vague.

## Source index

Full research provenance: [Parnas 1972](https://doi.org/10.1145/361598.361623) · [Ousterhout, APoSD notes](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) · [Ousterhout–Martin debate](https://github.com/johnousterhout/aposd-vs-clean-code/) · [Fowler, Refactoring 2e](https://martinfowler.com/articles/refactoring-2nd-changes.html) · [YAGNI](https://martinfowler.com/bliki/Yagni.html) · [Cognitive load essay](https://zakirullin.md/cognitive) · [Cognitive Complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf) · [Code Red](https://arxiv.org/abs/2203.04374) · [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) · [Semantic compression](https://caseymuratori.com/blog_0015) · [Carmack on inlining](https://cbarrete.com/carmack.html) · [grugbrain.dev](https://grugbrain.dev/) · [SlopCodeBench](https://arxiv.org/html/2603.24755v1) · [Show and Tell](https://arxiv.org/abs/2511.13972) · [To Add Is Machine](https://arxiv.org/html/2607.28887) · [TRACE](https://arxiv.org/html/2603.24586v2) · [IFScale](https://arxiv.org/html/2507.11538) · [SELF-REFINE](https://arxiv.org/abs/2303.17651) · [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Anthropic multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system) · [Claude Code commands](https://code.claude.com/docs/en/commands) · [Dynamic workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) · [Codemod](https://docs.codemod.com/workflows/introduction) · [Moderne](https://www.moderne.io/blog/ai-assisted-refactoring-in-the-moderne-platform) · [OpenHands parallel refactors](https://www.openhands.dev/blog/automating-massive-refactors-with-parallel-agents) · [Aider refactor bench](https://aider.chat/docs/leaderboards/refactor.html) · [WAVES](https://github.com/RayFernando1337/rayfernando-skills) · [Superpowers](https://github.com/obra/superpowers) · [Harness Engineering](https://blog.vtemian.com/post/harness-engineering/)

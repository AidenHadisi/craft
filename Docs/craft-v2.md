# craft v2 — Research and Redesign

Research-backed redesign of the `craft` plugin. The goal is higher-quality architecture and code with less ceremony, achieved by giving each agent one job and its own instructions, moving mechanical rules into tooling, and letting standards grow from real corrections instead of being guessed up front.

This document supersedes the standards design described in [craft-refactor.md](craft-refactor.md). That document's research on verbosity and deletion avoidance still holds; its conclusion — three shared standards files loaded by every agent — is what the evidence below argues against.

## The problem with v1

Craft v1 is an orchestrator skill plus four subagents (`craft-coder`, `craft-code-reviewer`, `craft-reviewer`, `craft-polisher`), all reading the same three files: `constitution.md` (12 hard MUST/NEVER rules), `principles.md` (93 lines of architecture and code-design judgment), and `testing.md`.

Four specific defects, in rough order of impact:

1. **No agent owns architecture.** Design happens in the orchestrator's context, which by that point holds exploration findings and the interview transcript. Architecture guidance is spread across `principles.md` and diluted into four agents that each need a different slice of it.
2. **The standards files fight the model.** They are long, partly self-evident, and internally contradictory (below).
3. **Parallel writers.** "All at once" mode dispatches disjoint Tasks to concurrent coders — the one place craft bets against coding-specific evidence.
4. **Uniform ceremony.** Two mandatory gates and a fixed phase list regardless of whether the change adds a subsystem or a column.

## What the evidence says

### Long instruction sets measurably lose compliance

No study directly compares "shared standards pack" against "per-agent instructions" for coding agents — that gap is real and worth stating plainly. What is measured is the underlying mechanism:

- [Instruction-stacking collapse](https://arxiv.org/html/2608.02639v1) scaled verifier-checked constraints from 1 to 20: follow rate fell from ~96% to ~60% (Sonnet 4.6), ~43% (Gemini), ~20% (GPT-5-mini). Failures came from **pairwise conflicts**, not uniform forgetting — roughly 12% of satisfiable pairs failed more than independence predicts.
- [IFScale](https://arxiv.org/abs/2507.11538) ([site](https://distylai.github.io/IFScale/)) shows accuracy declining with instruction density and a strong **primacy bias**: early instructions win. [Arize's 2026 replication](https://arize.com/blog/llm-instruction-following-benchmark-2026/) reports frontier models tracking far more named constraints than 2025 models — but capacity to *track* is not fidelity under *conflict*.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) and [Chroma's context rot](https://www.trychroma.com/research/context-rot) add position and length effects: mid-prompt rules compete poorly, and degradation appears well below the context limit.
- [Paradoxical interference](https://arxiv.org/pdf/2601.22047) is the most damaging result for v1: inserting constraints that the correct answer **already satisfied** hurt performance on math, QA, and code, including on Sonnet 4.5. Failing runs attended *more* to the constraints. Much of `principles.md` is guidance a strong model already follows.

### Anti-slop rules help the first cut and nothing after

[SlopCodeBench](https://arxiv.org/html/2603.24755) ([site](https://www.scbench.ai/)) had agents iteratively extend their own code under evolving contracts. Agent code was ~2.3× more verbose and ~2.0× more structurally eroded than human OSS baselines; erosion rose in ~77% of trajectories. Explicit anti-slop and plan-first guidance cut **initial** verbosity ~27–36% and erosion ~34–58% — while **leaving the degradation rate unchanged**.

Two consequences. A short constitution is worth keeping. And a dedicated later restructuring pass is justified on evidence rather than taste, which is why the polisher survives this redesign.

### Two of v1's hard rules are folklore, and they collide

- "Shared helpers only at 3+ call sites" and "nesting depth 3+ is a defect" have no supporting study. The nesting threshold traces to [Lizard's default, which cites Linux kernel indentation advice](https://github.com/terryyin/lizard/blob/master/theory.rst).
- They contradict each other: flattening deep nesting frequently wants a single-caller extraction, which the constitution forbids. This is exactly the pairwise-conflict failure mode above.

### Rules and examples do different jobs

[Show and Tell](https://arxiv.org/html/2511.13972) ran 160 two-turn sessions across four conditions. Directives ("minimal code that works") plus examples cut output ~70% versus control at turn one. Critically, at the enhancement turn **examples alone expanded just like the control** while directives held compression. Correctness stayed at ceiling throughout.

So: a few terse directives plus one or two exemplar files referenced by path — not a prose textbook, and not examples alone.

### Mechanical rules belong in tools

Anthropic's own guidance is that [CLAUDE.md is context, not enforcement, and hooks handle non-negotiables](https://code.claude.com/docs/en/claude-md); [Cursor's rules docs](https://cursor.com/docs/rules.md) say outright not to paste style guides and to use linters instead. Available deterministic coverage:

| Concern | Tool |
|---|---|
| Nesting depth, cyclomatic and cognitive complexity | [Lizard](https://github.com/terryyin/lizard), [Sonar cognitive complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf) |
| Dependency direction, layering, cycles | [dependency-cruiser](https://github.com/sverweij/dependency-cruiser), [go-arch-lint](https://github.com/fe3dback/go-arch-lint), [import-linter](https://import-linter.readthedocs.io/), [ArchUnit](https://www.archunit.org/) |
| Formatting, dead code, imports, naming | repo formatter and linter |
| Types and API shapes | compiler, `tsc`, mypy |

[Tweag's agentic coding handbook](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_AUTO_VALIDATIONS/) documents the loop: agent writes, the complexity check fails, the agent rewrites. Craft v1 ships no hooks at all, despite Cursor plugins supporting them.

### Single-threaded writes, isolated reviewers

Cognition's [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) argues parallel writers make conflicting **implicit** decisions that no brief captures. Their [follow-up](https://cognition.ai/blog/multi-agents-working) narrows the safe envelope: readonly search agents are fine, clean-context reviewers add real value, writes stay single-threaded. Anthropic's 90.2% multi-agent win was on breadth-first [research](https://www.anthropic.com/engineering/multi-agent-research-system), not shared mutable code — and their brief-quality lesson still applies, since vague briefs caused duplicated work.

On review efficacy, the strongest number available is vendor-measured: Cognition reports Devin Review finding ~2 bugs per PR with ~58% severe. Public review-tool league tables ([Greptile's](https://www.greptile.com/benchmarks) versus [AIMultiple's](https://aimultiple.com/ai-code-review-tools)) contradict each other and should be treated as marketing-adjacent.

Selection by judge is unreliable: [effort-halo bias](https://www.faros.ai/blog/llm-judge-coding-style-bias) puts best-of-N selection near chance without calibration, [verbosity bias](https://arxiv.org/abs/2310.10076) favors longer answers, and [agreeableness bias](https://aicet.comp.nus.edu.sg/wp-content/uploads/2025/10/Beyond-Consensus-Mitigating-the-agreeableness-bias-in-LLM-judge-evaluations.pdf) yields true-negative rates often under 25%. **Tests select; judges advise.**

### Learning loops: append deltas, never rewrite the rulebook

[ACE](https://arxiv.org/abs/2510.04618) ([site](https://ace-agent.github.io/)) is the closest published match to what craft needs: a Reflector extracts lessons from trajectories, a Curator emits **itemized delta bullets**, and merge, dedup, and prune run in **non-LLM code**. It explicitly targets *context collapse* — the failure where an LLM rewriting a whole playbook silently erases detail — and *brevity bias*. Measured +10.6% on AppWorld agents and +8.6% on finance, with roughly 82% lower adaptation latency than [GEPA](https://arxiv.org/abs/2507.19457).

Supporting patterns worth stealing: [AutoGuide](https://arxiv.org/abs/2403.08978) makes each lesson conditional — *when state S, do A* — and retrieves by current state, beating undifferentiated insight dumps ([ExpeL](https://arxiv.org/abs/2308.10144)). [Dynamic Cheatsheet](https://arxiv.org/abs/2504.07952) shows large gains from a curated reusable store. [Reflexion](https://arxiv.org/abs/2303.11366) and [Self-Refine](https://arxiv.org/abs/2303.17651) are intra-task and do not produce durable cross-task rules.

Harness reality: Cursor **removed IDE Memories** around 2.1.17 and now frames [Rules](https://cursor.com/docs/rules.md) as the persistence layer; agents write `.mdc` files directly. Both Cursor and [Codex](https://developers.openai.com/codex/guides/agents-md) advise adding a rule only after a **repeated** mistake, keeping files scoped, and staying under 500 lines.

### Everyone who built elaborate pipelines added a fast lane

[Spec Kit](https://github.github.io/spec-kit/) runs constitution → specify → clarify → plan → checklist → tasks → analyze → implement, and practitioners note it has [no genuinely light path](https://arceapps.com/blog/sdd-frameworks-analysis-spec-kit-openspec-bmad/). BMAD's persona chain drew [explicit requests for simplification](https://github.com/bmad-code-org/BMAD-METHOD/issues/555) and later gained Quick Flow; [Kiro](https://kiro.dev/docs/specs/) added Quick Spec; [Traycer](https://docs.traycer.ai/tasks/phases) lets you skip phases. One timed anecdote ([Reenbit](https://reenbit.com/bmad-vs-spec-kit-vs-openspec-choosing-your-spec-driven-ai-framework/)) put the same CRM task at 12 minutes under OpenSpec, 90 under Spec Kit, and 5.5 hours under BMAD.

The reason they needed second paths is that **their phases are fixed-cost artifacts** — BMAD's Architect phase means an architecture document, with no cheap version. Craft's phases are prompts, so cost can scale with the work and a second path is unnecessary. What cannot scale smoothly is a *gate*, which is binary; gates need an objective trigger.

### Role specialization is the norm; instruction sharing is the open question

Per-role instructions are standard practice: [BMAD](https://docs.bmad-method.org/reference/workflow-map/) personas, [OpenHands](https://docs.openhands.dev/sdk/guides/agent-file-based) file-defined agents with distinct prompts and tools, [Factory droids](https://docs.factory.ai/harness/subagents), [Amp custom agents](https://ampcode.com/news/custom-agents), Task Master's orchestrator/executor/checker split, and [Superpowers](https://github.com/obra/superpowers)' fresh implementer plus separately-templated reviewer. Notably, [Agent OS retired](https://buildermethods.com/agent-os/migration) its roles/implementers/verifiers system as overbuilt and replaced it with injecting only the *relevant subset* of standards.

For keeping duplicated instructions honest, the mature pattern is compile-from-fragments ([AgentQuilt](https://github.com/daxdue/agentquilt), [Google's modular prompt transpilation](https://developers.googleblog.com/en/building-scalable-ai-agents-with-modular-prompt-transpilation/)). v2 chooses a simpler option that avoids a build step.

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Instruction ownership | One instruction file per role, owned by that role. No shared standards pack. | Removes role-irrelevant rules from every prompt; avoids a build step and a drift checker |
| Architecture ownership | New `craft-architect` agent owns the design phase; its output is what the user approves | Nothing owned architecture in v1 — the top complaint |
| Standards size | Roughly eight always-on lines, inlined verbatim into every writing agent | Anti-slop directives measurably help; density measurably hurts |
| Numeric thresholds | Deleted from prompts; enforced by lizard, arch-fitness tools, and linters via hooks | Unmeasured folklore that conflicts with other rules; tools decide these exactly |
| Parallel writes | Allowed only for genuinely file-disjoint tasks with contracts pinned in the plan | Cognition's implicit-decision failure mode is real, but total serialization is too slow |
| Path | One path with elastic phases | Fixed-cost phases are why other frameworks needed a second path |
| Design gate | Fires when a boundary is created or moved | A gate is binary; letting the agent judge ceremony reproduces the inconsistency problem |
| Plan gate | Agent review loop, then user approval — both kept | The cheapest place to catch a wrong design is before code exists |
| Standards origin | Start near-empty; grow only from real corrections | Guessed rules are the current failure; Cursor and Codex both advise growing from repeated mistakes |
| Learning mechanism | Delta lessons with triggers, proposed as a diff, deterministic merge, periodic gardener pass | ACE's grow-and-refine; avoids context collapse |
| Selection and verdicts | Tests and checks select; agent reviewers advise | Judge bias makes LLM selection near chance without calibration |
| Measurement | A small benchmark of real tasks plus a correction log | None of this is settled by literature |

## The design

### Agents

Four agents, each with a single job and a self-contained instruction file. No agent reads another agent's instructions, and no agent reads a shared standards directory.

| Agent | Owns | Instruction content |
|---|---|---|
| `craft-architect` | Design candidates and the boundary decisions behind them | Architecture judgment only: decision-hiding, deep modules, repo fit, one-way coupling, likely-change containment |
| `craft-coder` | Writing code for one assignment | Write-time directives, brief fidelity, scope discipline |
| `craft-reviewer` | Pass/Revise on a plan or a diff, in clean context | A rubric: checkable criteria, severity definitions, anti-nitpick and anti-length-bias framing |
| `craft-polisher` | Restructuring a working diff | Refactoring judgment and simplification order |

`craft-reviewer` merges v1's `craft-reviewer` and `craft-code-reviewer`. They differed in what they were handed (plan text versus diff), not in how they think, and both need the same bias correction. One rubric agent with two input modes is less to maintain and less to drift.

Only `craft-coder` and `craft-polisher` write; `craft-architect` and `craft-reviewer` are `readonly: true`.

The orchestrator skill keeps judgment and gates, dispatches exploration to generic readonly subagents, and writes every shared artifact. Cursor caps subagent nesting one level deep, so craft's agents must not rely on spawning their own children.

### Instruction ownership

Each agent's `.md` file contains everything it needs. The one exception is the always-on block, short enough to inline verbatim in all four files — roughly eight lines covering: least code that stays clear; no speculative generality; validate only at boundaries; never swallow errors; prefer stdlib and existing dependencies; stay inside the requested behavior; verify unfamiliar APIs against the repo or docs; report what was deleted and deliberately not added.

Every other rule lives in exactly one agent's file. Architecture judgment appears only in the architect. The simplification order appears only in the polisher. The review rubric appears only in the reviewer. Nothing is duplicated, so nothing can drift.

`principles.md`, `constitution.md`, and `testing.md` are deleted. Their load-bearing content is redistributed; the self-evident and folkloric content is dropped.

### Deterministic spine

The plugin ships `hooks/hooks.json`. Available events include `afterFileEdit`, `postToolUse` (with `additional_context` to feed results back), `beforeShellExecution`, `subagentStop` and `stop` (with `followup_message` and a default loop limit of five), and `failClosed` to block on hook failure — see [Cursor hooks](https://cursor.com/docs/hooks.md).

Three layers:

1. **After every edit** — the repo's formatter and linter, plus type checking where it is cheap. Failures return as `additional_context` so the agent fixes them without a human in the loop.
2. **Per wave** — complexity check via lizard when available, and any arch-fitness tool the repo already has configured. Violations are hook output, not reviewer opinion.
3. **Offered, never imposed** — in a repo with no arch-fitness tooling, craft may propose adding it as an explicit plan Task. It never installs tooling silently.

Hooks handle mechanics so prompts can spend their limited attention on judgment. Anything a tool can check is not stated as a rule.

### One path, elastic phases

```
understand → interview → design → [design gate] → plan → plan review → [plan gate]
  → build (implement + review waves) → polish → verify → offer live test
```

Every phase always runs; its cost scales with the work. On a two-file change with no new seam, the architect returns one design in a paragraph, the plan is ten lines, and the reviewer reads a small diff.

**The design gate fires when the change creates or moves a boundary:** a new module, package, public interface, database table, endpoint, wire contract, or cross-layer dependency. Otherwise the design flows straight into the plan. The trigger is a property of the change rather than a judgment about its size, so it behaves the same way every time.

**The plan gate always fires** after the reviewer reaches Pass.

**Parallel writes** are allowed only when tasks touch strictly disjoint files *and* every shared contract between them is pinned in the plan — signature, wire shape, error values. If either condition fails, the tasks run in sequence. This narrows Cognition's failure mode to cases where the implicit decisions have been made explicit in advance.

### The learning loop

A new skill, `/craft-learn`, invoked as "don't make this mistake again" with the correction in context.

Each lesson is one record:

```markdown
- id: prefer-existing-http-client
  role: coder
  trigger: files matching **/*.go that make outbound HTTP calls
  wrong: hand-rolled http.Client with custom retry
  right: use internal/httpx.Client — it owns timeouts and retry
  evidence: <commit or diff snippet from the correction>
  source: user correction, 2026-08-08
```

Flow:

1. The skill reads the correction and identifies **which role** made the mistake. Lessons route to that role's file, so a coder mistake never lands in the architect's instructions.
2. It drafts a **delta**: one appended bullet, never a rewrite of the role's file. Monolithic rewrites are how ACE's context collapse happens.
3. It presents the diff. Nothing is written until approved.
4. Merge and dedup are mechanical: identical triggers collapse, and a lesson already implied by the always-on block is rejected rather than added.

`/craft-garden` runs the consolidation pass on demand: merge near-duplicates, promote a lesson seen three or more times into the role's core instructions, demote always-on lessons to trigger-scoped ones, and delete lessons that no longer describe a real failure. This is ACE's grow-and-refine, human-gated.

**Standards start near-empty.** Beyond the eight always-on lines and the minimum each role needs to do its job at all, every rule earns its place by being a mistake that actually happened.

### Measurement

Two signals, both cheap:

- **A task benchmark.** Five to ten real features already built with craft, kept as prompts alongside their outcomes. Re-run a few after significant changes and compare the diffs directly. This is the only defense against the failure mode this document diagnoses: rules that felt right and made things worse.
- **A correction log.** Every `/craft-learn` invocation is a datapoint. Corrections per feature trending down is the signal that the loop works; the same lesson recurring after being recorded means the rule is not being followed and belongs in a hook instead.

## Migration

1. Write `craft-architect`; move architecture judgment out of `principles.md` into it, dropping what is self-evident.
2. Merge `craft-code-reviewer` into `craft-reviewer` as a rubric with two input modes.
3. Rewrite `craft-coder` and `craft-polisher` as self-contained files; inline the always-on block into all four agents.
4. Delete `standards/`.
5. Add `hooks/hooks.json` with the format, lint, and typecheck layer; add the complexity and arch-fitness layer once the first is stable.
6. Rewrite `skills/craft/SKILL.md` around the single elastic path and the boundary-triggered design gate.
7. Add `/craft-learn` and `/craft-garden`, plus empty per-role lesson sections.
8. Capture the benchmark tasks before the rewrite lands, so there is a v1 baseline to compare against.

Steps 1 through 4 are one coherent change and should land together. Steps 5 through 8 are independent.

## Risks

| Risk | Mitigation |
|---|---|
| The per-agent split is a hypothesis, not a proven result | The benchmark exists precisely to catch this, and the split is cheap to reverse |
| Lesson files become the next bloated constitution | Triggers scope retrieval, the gardener pass prunes, and promotion requires three occurrences |
| Hooks slow every edit or fail noisily | Start with format and lint only; add complexity checks per wave rather than per edit |
| The boundary trigger for the design gate is gamed or misjudged | The trigger lists concrete artifacts — module, interface, table, endpoint, cross-layer dependency — not a size judgment |
| Narrow parallel writes still collide | Requires both disjoint files and pinned contracts; anything short of that serializes |
| Deleting `principles.md` loses real judgment | Content is redistributed rather than discarded, and anything genuinely missed reappears as a correction and is re-added with evidence |

## Open questions

- Whether `craft-architect` should ever run as competing designers on high-stakes features. The literature warns that judge-based selection is near chance, so any best-of-N would need selection by contract satisfaction rather than by a reviewer's preference. Deferred until the single-architect version has a track record.
- Whether the always-on block belongs in the agent files at all, or in a plugin-shipped always-apply rule. Inlining is chosen for now because it stays visible in the file being edited.
- Whether lessons should be stored as Cursor `.mdc` rules with globs — which would give free scoped retrieval — instead of sections inside agent instruction files. Rules apply to the main agent's context and it is under-specified whether user rules reach subagents, so agent-file storage is safer until that is confirmed.

## Source index

Instruction following and context: [Instruction-stacking collapse](https://arxiv.org/html/2608.02639v1) · [IFScale](https://arxiv.org/abs/2507.11538) · [Arize 2026 replication](https://arize.com/blog/llm-instruction-following-benchmark-2026/) · [Lost in the Middle](https://arxiv.org/abs/2307.03172) · [Context rot](https://www.trychroma.com/research/context-rot) · [LongProc](https://arxiv.org/abs/2501.05414) · [Paradoxical interference](https://arxiv.org/pdf/2601.22047) · [Unclear requirements](https://arxiv.org/html/2507.20439v1)

Code quality under generation: [SlopCodeBench](https://arxiv.org/html/2603.24755) · [Show and Tell](https://arxiv.org/html/2511.13972) · [To Add Is Machine, To Delete Is Human](https://arxiv.org/html/2607.28887) · [TRACE](https://arxiv.org/html/2603.24586v2) · [Lizard complexity theory](https://github.com/terryyin/lizard/blob/master/theory.rst) · [Cognitive Complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)

Judges and review: [Verbosity bias](https://arxiv.org/abs/2310.10076) · [Judging the Judges](https://arxiv.org/html/2604.23178) · [Effort halo](https://www.faros.ai/blog/llm-judge-coding-style-bias) · [Agreeableness bias](https://aicet.comp.nus.edu.sg/wp-content/uploads/2025/10/Beyond-Consensus-Mitigating-the-agreeableness-bias-in-LLM-judge-evaluations.pdf) · [CR-Bench](https://www.arxiv.org/pdf/2603.11078)

Multi-agent architecture: [Cognition, Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) · [Cognition, What's Actually Working](https://cognition.ai/blog/multi-agents-working) · [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Anthropic multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system)

Self-improving context: [ACE](https://arxiv.org/abs/2510.04618) · [AutoGuide](https://arxiv.org/abs/2403.08978) · [Dynamic Cheatsheet](https://arxiv.org/abs/2504.07952) · [ExpeL](https://arxiv.org/abs/2308.10144) · [GEPA](https://arxiv.org/abs/2507.19457) · [Reflexion](https://arxiv.org/abs/2303.11366) · [Self-Refine](https://arxiv.org/abs/2303.17651) · [Voyager](https://arxiv.org/abs/2305.16291)

Workflows and harnesses: [Spec Kit](https://github.github.io/spec-kit/) · [BMAD](https://docs.bmad-method.org/reference/workflow-map/) · [Agent OS migration](https://buildermethods.com/agent-os/migration) · [Kiro specs](https://kiro.dev/docs/specs/) · [Traycer phases](https://docs.traycer.ai/tasks/phases) · [Superpowers](https://github.com/obra/superpowers) · [Tweag auto-validations](https://tweag.github.io/agentic-coding-handbook/WORKFLOW_AUTO_VALIDATIONS/) · [AgentQuilt](https://github.com/daxdue/agentquilt) · [Google modular prompt transpilation](https://developers.googleblog.com/en/building-scalable-ai-agents-with-modular-prompt-transpilation/)

Cursor and harness mechanics: [Plugins](https://cursor.com/docs/plugins.md) · [Skills](https://cursor.com/docs/skills.md) · [Subagents](https://cursor.com/docs/subagents.md) · [Rules](https://cursor.com/docs/rules.md) · [Hooks](https://cursor.com/docs/hooks.md) · [Claude CLAUDE.md guidance](https://code.claude.com/docs/en/claude-md) · [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md) · [Amp custom agents](https://ampcode.com/news/custom-agents)

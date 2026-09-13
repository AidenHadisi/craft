# Autonomous, role-based coding pipelines: what works, what is theater, and what it means for craft

Research into how developers run "teams of AI agents with roles" to automate coding while keeping quality high, and what a single Cursor user can adopt. Sources are inline. Written September 2026.

## The picture

Stripped of marketing, nearly every setup that ships real software converges on one skeleton:

1. Force intent clarification before any code, and write it down.
2. Turn that intent into a plan of small, independently verifiable slices, stored as files in the repo.
3. Execute each slice in a fresh-context worker that receives a constructed brief, not conversation history.
4. Gate "done" with something the agent cannot argue with: tests, build, lint, a live run.
5. Review each slice in a separate context from the one that wrote it.
6. Keep resumable state outside the chat (ledger, progress, decisions), because compaction will eat the conversation.
7. Put humans at intent, plan, and PR. Everything in between is autonomous with a logged decision, and escalation is exception-only.

The "roles" people post about are mostly this skeleton with job titles attached. Where the titles add a new source of information (a live tester), a forcing function (a spec that must be approved), or a fresh context (an independent reviewer), they help. Where they only relabel the same context ("you are now the CEO"), they are theater and often net negative. The most-quoted failure in the field is a CEO agent that, given broad authority, created twenty roles and had the team writing memos to each other within hours while work stopped ([HN, yego](https://news.ycombinator.com/item?id=47245373)).

The community's verdict on every heavyweight framework is identical: excellent on large ambiguous work, a token furnace on small work. The load-bearing pieces are few and cheap. The overhead is ceremony.

## Findings by area

### 1. What developers are actually running

Setups with credible first-hand accounts, and what each contributes:

| Setup | Shape | Distinctive idea | Reported failure |
|---|---|---|---|
| [superpowers](https://github.com/obra/superpowers) (obra) | brainstorm → plan → fresh subagent per task → two-stage review → finish | Skills as mandatory process; a session-start "using-superpowers" skill with a rationalization red-flags table; ledger for resumability; model tiering | Slow and expensive on trivial edits ([review](https://dev.to/aidiveyt/superpowers-fixes-claude-code-then-it-bills-you-for-every-two-line-fix-6dg)) |
| [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) | analyst → PM → architect → SM shards stories → dev → QA | Story file as a context-packing device; v6 dropped personas and added right-sizing | Waterfall, 1000+ lines of docs for small tasks ([r/BMAD_Method](https://www.reddit.com/r/BMAD_Method/comments/1r6aruo/bmad_method_sucks/)) |
| [spec-kit](https://github.com/github/spec-kit) | constitution → specify → clarify → plan → tasks → implement → converge | The `specs/` directory is the whole state; any agent cold-starts from files | "Illusion of work" ([discussion #1784](https://github.com/github/spec-kit/discussions/1784)); spec/code drift |
| [Kiro](https://kiro.dev/docs/specs/) | requirements (EARS) → design → tasks, human-approved each | EARS acceptance criteria; requirement→task traceability; Quick Spec skips gates for crisp work | Rigid; no milestone pauses during execution |
| [Agent OS v3](https://buildermethods.com/agent-os) | standards + product + spec shaping only | Deleted its own orchestration; kept context injection | Modest gains, creator-led evidence |
| [Ralph loop](https://ghuntley.com/ralph/) (Huntley) | `while :; do cat PROMPT.md \| claude -p; done` | One item per loop, fresh context each loop, tests as backpressure; state entirely in files | Greenfield only by the author's own account; 90% ceiling; prompt bloat makes the agent "slower and dumber" ([repomirror](https://github.com/repomirrorhq/repomirror/blob/main/repomirror.md)) |
| [beads](https://github.com/steveyegge/beads) / Gas Town (Yegge) | git-backed dependency-aware issue graph; 20–30 agents | `bd ready` for unblocked work; agents killed after each issue | 240k lines of unmaintainable tooling; "insane merge queues" at 12 agents; author settled at 1–3 |
| [compound engineering](https://every.to/guides/compound-engineering) (Every) | brainstorm → plan → work → simplify → review → compound | Fourth step writes learnings to `docs/solutions/`; 80% of human time on plan + review | Testimony only, no measurement |
| yego's 3-agent Docker setup | backend / frontend / CEO (forbidden to code), sequential, `docs/tasks/*.md` | `lessons-learned.md` "saved more time than anything else" | The CEO incident above |
| [claude-flow / ruflo](https://github.com/ruvnet/ruflo) | swarms, consensus, "neural" learning | — | Audits found core features stubbed, `Math.random()` accuracy, self-reported success at 89% failure ([issue #1326](https://github.com/ruvnet/ruflo/issues/1326)) |

Cross-cutting: markdown files are the API between agents; the main agent is a scheduler, not a worker; reviewer ≠ implementer; sequential for coupled work, parallel only for independent exploration/review; a persistent lessons file is the highest-ROI artifact; spec↔code drift is unsolved everywhere.

Skeptics worth weighing: the [METR RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) (experienced devs 19% slower with AI while believing 20% faster); [Cognition's "Don't Build Multi-Agents"](https://cognition.ai/blog/dont-build-multi-agents) and its [2026 follow-up](https://cognition.com/blog/multi-agents-working) (multi-agent works only when writes stay single-threaded and extra agents contribute intelligence, not actions); [GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research) (duplication up ~8x, refactoring down); Anthropic's own note that coding has far fewer truly parallelizable subtasks than research ([multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)).

### 2. Which roles add quality, and which are theater

The research literature separates cleanly once you ask what each "role" adds:

| Separation | Verdict | Evidence |
|---|---|---|
| Spec written before code | Strong | Requirement clarity is the codegen bottleneck ([Requirements are All You Need](https://arxiv.org/abs/2406.10101)); ambiguous prompts drop Pass@1 20–40% (Larbi et al. via [Kiro](https://kiro.dev/blog/deep-spec-analysis/)); Anthropic's planner prevented under-scoping ([harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)) |
| A separate *PM agent* writing it | Weak | No study isolates the agent from the artifact. The value is the file plus the human gate |
| Separate planner/architect | Medium-high, conditional | Aider's architect/editor split beats solo even same-model (80.5 vs 77.4; R1+Sonnet SOTA at 14x lower cost, [aider](https://aider.chat/2024/09/26/architect.html)); pays off when the plan is checked or survives context resets |
| Fresh-context reviewer vs self-review | Strongest in the literature | Self-correction without external signal degrades output ([Huang et al.](https://arxiv.org/abs/2310.01798)); LLMs can't find their own errors but fix located ones ([Tyen et al.](https://arxiv.org/abs/2311.08516)); 31.7% of semantic-drift outputs silently endorsed by their own author ([Articulate but Wrong](https://arxiv.org/html/2605.21537v1)); Devin Review catches ~2 bugs/PR, 58% severe, only with no shared context ([Cognition](https://cognition.com/blog/multi-agents-working)) |
| Adversarial critic with a rubric | Medium | Helps with heterogeneity or ground truth. Anthropic: "tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work" |
| Homogeneous multi-agent debate | Theater | Loses to self-consistency at matched compute ([Stop Overvaluing MAD](https://arxiv.org/abs/2502.08788), [Cost of Consensus](https://arxiv.org/abs/2605.00914)) |
| Independent tester that runs the code | Very strong | AgentCoder's independent test designer beat single agents across 14 LLMs at lower cost ([paper](https://arxiv.org/abs/2312.13010)); Anthropic's Playwright evaluator caught bugs invisible from code ([harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)); "out of the box, Claude is a poor QA agent" and must be tuned skeptical |
| Many narrow roles | Negative past ~3 | Dong et al.: coder 45 → +analyst 55 → +tester 64 → +4th role ~+1 ([self-collaboration](https://arxiv.org/abs/2304.07590)); MAST: multi-agent systems fail 41–87% of tasks, mostly on specification, coordination and verification ([Why do MAS fail](https://arxiv.org/abs/2503.13657)) |
| Per-role model tiering | Medium-high | Model upgrade beat doubling token budget (Anthropic); cheap models can cost more via turn count (superpowers); a weak model cannot know when it is stuck, so escalation must be a deterministic rule, not the worker's judgment ([Cognition smart-friend](https://cognition.com/blog/multi-agents-working)) |

The unifying rule: a separation earns its cost only if it adds new information (execution results, fresh eyes), a forcing function (an approved spec, a failing test, a rubric with thresholds), or context budget (isolation). Otherwise merge it. Communication between roles should be files for content and small structured returns for control; never paste history into a dispatch ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), [MetaGPT](https://arxiv.org/abs/2308.00352), superpowers).

One caution: Anthropic observed its own harness components going stale between model generations (sprint decomposition needed for Opus 4.5, dropped for 4.6). Separations that compensate for model weakness depreciate; separations that add verification do not.

### 3. Orchestration for one task, unattended, to PR

Patterns and their tradeoffs:

- **Linear phase pipeline** (spec → plan → build → review → test): predictable and resumable; a bad plan poisons everything downstream. Fix: a gate on the plan.
- **Slice loop**: ledger of slices, each run in a fresh coder → gate → fresh review → commit. Blast radius is one slice; natural resume point. This is the shape Anthropic, superpowers, and beads all converged on.
- **Loop-until-done (Ralph)**: powerful for greenfield ports and mechanical translation; the author himself will not use it in an existing codebase.
- **Generator/critic**: measurable lift with clear criteria; an unscoped reviewer always finds something and drives over-engineering. Scope it to correctness and stated requirements.

What makes a good slice: small (superpowers uses 2–5 minute tasks with exact paths and complete code; [12-factor](https://github.com/humanlayer/12-factor-agents) says 3–10 steps), vertical, and carrying its own verification command so the loop closes without human judgment. Anthropic found JSON feature lists with `passes: false` survive agent edits better than markdown, and needed explicit "it is unacceptable to remove or edit tests" language.

Parallelism: on for read-only exploration and review, off by default for writes. Only slices with disjoint file sets and no interface dependency may run concurrently, each in its own worktree, merged sequentially. Cursor supports this with `/worktree`, `agent --worktree`, and cloud VMs ([worktrees](https://cursor.com/docs/configuration/worktrees)).

Stuck detection: retry budget of 2–3 per slice, each retry in fresh context with the failure evidence appended (a polluted context does not recover, [Claude Code best practices](https://code.claude.com/docs/en/best-practices.md)); then one escalation to a stronger model; then stop, write findings to the ledger, and report. Fail closed on destructive or ambiguous actions.

State: the ledger, progress log, decision log, spec, and git history are the entire cross-session memory. Anthropic's session-opening ritual is worth copying: read progress → read git log → read feature list → run a baseline check → pick the next unfinished item ([harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

Orchestrator thickness: the trend is toward a thin controller that decomposes, dispatches, and synthesizes, with control flow as deterministic as possible. Boris Cherny (Claude Code): "My job is to write loops" ([thread](https://threadreaderapp.com/thread/2007179832300581177.html)). The orchestrator should not fix code itself; superpowers is explicit that controller fixes pollute context and skip review.

### 4. Quality gates, ranked by evidence

1. **Deterministic executable checks wired into the loop** (tests, build, lint, typecheck as hooks, not prompts). Cheapest quality per dollar. Both vendors converge: give the agent a check it can run; hooks are deterministic while instruction files are advisory ([Claude Code](https://code.claude.com/docs/en/best-practices.md), [Codex](https://developers.openai.com/codex/learn/best-practices)). Agents skip advisory steps under pressure ([superpowers #384](https://github.com/obra/superpowers/issues/384)).
2. **Live end-to-end verification by a separate evaluator.** Anthropic's solo build ($9, 20 min) shipped a silently broken core feature; the harnessed build ($200, 6 h) worked. Static checks miss 19–35% of non-equivalent LLM refactorings ([differential fuzzing](https://arxiv.org/html/2602.15761)). Expensive; worth it for anything user-facing.
3. **Frozen spec with testable acceptance criteria.** Strong practitioner convergence, no RCT. Keep the spec high-level; detailed technical errors in the spec cascade.
4. **Fresh-context code review with a gap-focused rubric.** Cursor's Bugbot went 52% → 76% resolution rate by optimizing a ground-truth metric and using majority voting across shuffled passes ([Bugbot](https://cursor.com/blog/building-bugbot)). Diminishing returns after 1–3 rounds.
5. **Tests-first, with anti-gaming hardening.** Real benefit, real failure mode: METR observed reward hacking 43x more often when the scoring function was visible ([METR](https://metr.org/blog/2025-06-05-recent-reward-hacking/)); a `conftest.py` hook can pass nearly all of SWE-bench ([BenchJack](https://arxiv.org/html/2605.12673)). Protect test files, verify RED before GREEN, hold out tests where possible.
6. **Definition-of-done frozen up front** as a machine-checkable artifact. Cheap.
7. **Adversarial design critique before building.** Plausible, weakest direct measurement.
8. **Polish/simplification pass.** The problem is well measured (AI code is 1.7x more defective and 3x less readable, [CodeRabbit](https://www.theregister.com/software/2025/12/17/ai-authored-code-needs-more-attention-contains-worse-bugs/2576263)); the pass is itself a drift risk, so gate it with the same checks.
9. **LLM-as-judge scoring.** Weakest standalone: 33–41 point kappa deflation, ranking instability ([Reliability without Validity](https://arxiv.org/html/2606.19544v1)). Use only where no deterministic check exists.

Failure modes to design against: reward hacking, sycophantic reviewers, scope creep and premature "done", hallucinated packages (~20% of suggested packages across 16 models, [USENIX](https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf)), silent behavior changes, and overconfidence. The common mitigation is evidence over assertion: never let the agent's prose be the only proof of verification.

### 5. Persistent memory

The filesystem is the memory; context is a budget. Layers ordered by half-life:

| Layer | Location | Holds | Always-on? |
|---|---|---|---|
| User rules | Cursor user rules | Cross-project preferences only | Yes, tiny |
| Repo constitution | `AGENTS.md` | Non-inferable facts: exact commands, non-default conventions, pitfalls, pointers to other layers. Under 200 lines | Yes |
| Scoped rules | `.cursor/rules/*.mdc` | Module conventions, glob- or description-scoped | No |
| Skills | `.cursor/skills/` | Procedures and "sometimes" knowledge; progressive disclosure via `references/` | Description only |
| Active plan | `docs/plans/<feature>.md` | Goal, architecture, progress checklist, surprises, decision log, retrospective ([OpenAI ExecPlan](https://github.com/openai/openai-agents-python/blob/33b9a2c9fd5b6be8af45cac9a1a266953f3977f2/PLANS.md)) | Only when working it |
| Learnings | `docs/solutions/` | One file per lesson, indexed, dated; written right after a task ([compound engineering](https://every.to/guides/compound-engineering)) | No |
| Decision log | `docs/decisions/` | Contested decisions only; immutable, superseded not edited | No |

The always-on budget matters more than anything else in this table. The one rigorous study of instruction files ([ETH Zurich, ICLR 2026](https://arxiv.org/abs/2602.11988)) found LLM-generated AGENTS.md files *reduce* success ~3% and raise cost >20%, while minimal human-written files gain only ~4%. Agents do follow instructions, which is exactly why bloat hurts. Test for every line: would removing it cause a mistake?

Agent-written memory rots unless governed: caps, timestamps, indexes, supersession, and a periodic refresh pass. Yegge accumulated 605 decaying plan files before building beads; Every ships `/ce-compound-refresh` for the same reason. Cursor's native Memories feature was removed in 2.1.x ([forum](https://forum.cursor.com/t/are-my-memories-gone/144057)); do not build on it.

### 6. Human touchpoints

The empirical picture on unattended runs is sobering. In 20,574 real sessions, the dominant failures were interaction-level, not code-level: constraint violation 38%, misread intent 27%, inaccurate self-reporting 23%; 91.5% of visibly resolved failures required explicit developer pushback and only 3% self-corrected ([How Coding Agents Fail Their Users](https://arxiv.org/html/2605.29442v1)). Of 33,596 agent-authored PRs, 28.5% never merged, and the top cause was reviewer abandonment at 38%, then duplicates 23% ([MSR 2026](https://doi.org/10.48550/arxiv.2601.15195)). Roughly 2% of sessions showed monitor evasion or fabricated verification claims ([Transluce](https://transluce.org/docent/blog/coding-agent-behaviors)).

Two consequences. First, unattended runs remove the mechanism that catches nine out of ten failures, so the pipeline must replace it structurally with gates and independent verification. Second, review cost is the PR-stage killer, so the PR must be self-explaining and small.

Recommended touchpoints:

- **T0 Interview** (2–5 min): agent restates the goal, then one batched round of forced-choice questions with recommended defaults. Output is a frozen brief: goal, testable acceptance criteria, constraints, non-goals, architecture preference, verification method, risk tier. Skip or shrink for crisp low-risk work. Interview answers must be rendered from actual user input; Transluce's worst case was an agent fabricating sixteen user decisions when its question tool returned empty.
- **T1 Plan gate** (~2 min, async): files touched, patterns reused, blast radius, test strategy mapped to criteria, resolved ambiguities. The highest-leverage gate in the pipeline; it kills wrong-problem, duplicate, and unwanted-feature failures for the price of a short read.
- **T2 Exception escalation** (rare): spec-changing ambiguity, irreversible design forks, necessary scope expansion, exhausted retry budget, sandbox-boundary crossings, any weakening of tests or checks. Everything else is decide-and-log.
- **T3 PR review** (target ≤10 min): built-vs-criteria mapping, machine-generated evidence (CI, test output, screenshots), decision log, deviations, what was not verified, an independent automated review already done.
- **T4 Merge** is human-only. Agents never self-merge.
- **T5 Calibration** (periodic): spot-check decision logs against reality; a ~100% approval rate at a gate means rubber-stamping. Complacency is not fixable by training ([Parasuraman & Manzey](https://journals.sagepub.com/doi/10.1177/0018720810376055)); it has to be engineered around.

Anthropic's telemetry shows experienced users migrate from approve-everything to monitor-and-intervene, and agents on hard tasks ask for clarification more than twice as often as humans interrupt them ([Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy)). Preserve the agent-initiated stop; do not mandate per-action approval.

### 7. What Cursor gives you

From the 2026 docs ([cursor.com/llms.txt](https://cursor.com/llms.txt)):

- **Subagents**: `agents/*.md` in a plugin or `.cursor/agents/`; frontmatter `model`, `readonly`, `is_background`. Two-level nesting (main → subagent → child, no deeper). Background, resumable by ID, cloud via `/in-cloud`. Isolation via worktree or VM on request. No documented `tools` allowlist in markdown frontmatter; plugin agent files are documented with only `name` and `description`, so `model`/`readonly` in plugin agents is unverified ([subagents](https://cursor.com/docs/subagents.md), [plugins reference](https://cursor.com/docs/reference/plugins.md)).
- **Skills**: `SKILL.md` with `references/`, `scripts/`, `paths`, `disable-model-invocation`. A skill cannot mechanically invoke another skill; the agent follows prose ([skills](https://cursor.com/docs/skills.md)).
- **Hooks**: `.cursor/hooks.json` (project) or `hooks/hooks.json` (plugin). Events include `preToolUse`, `postToolUse`, `beforeShellExecution`, `afterFileEdit`, `subagentStart`, `subagentStop`, `stop`, `preCompact`. `stop`/`subagentStop` can return a `followup_message` to loop until a check passes (default `loop_limit` 5). `beforeShellExecution` can deny `git commit`/`git push`. `preToolUse` can deny edits. No dedicated commit hook; cloud runs only project hooks ([hooks](https://cursor.com/docs/hooks.md)).
- **Cloud Agents / Automations**: launch from chat, Slack, GitHub, Linear, API; open PRs; artifacts (screenshots, logs) attach to the PR; autofix CI on own PRs. Automations trigger on cron, SCM events, webhooks; per-automation `MEMORIES.md` ([cloud agent](https://cursor.com/docs/cloud-agent.md), [automations](https://cursor.com/docs/cloud-agent/automations.md)).
- **CLI / SDK**: `agent -p --output-format json --worktree`, `--resume`; SDK `Agent.create`, `Agent.resume`; hooks file-based only ([CLI](https://cursor.com/docs/cli/overview.md), [SDK](https://cursor.com/docs/sdk/typescript.md)).
- **Bugbot**: `.cursor/BUGBOT.md` rules; check is `neutral` by default when findings exist, `failure` only if the org enables fail-on-unresolved ([bugbot](https://cursor.com/docs/bugbot.md)).

Undocumented, do not design around: skill-to-skill invocation, a numeric subagent concurrency cap, IDE project memories, plugin agents honoring `model`/`readonly`.

## Implications for craft

### Where craft stands

Craft already has the right role set: coder, critic, plan reviewer, code reviewer, polisher, tester, researcher, all fresh-context, all returning structured results. That is the hard part, and most of the frameworks above took years to get there. The choppiness comes from the layer around them:

- Two entry points (`craft`, `craft-auto`) with drifted templates, two plan formats, and inconsistent finish behavior (one asks before testing and does not PR; the other always tests and PRs).
- Two critique roles (`craft-reviewer` for plans, `craft-critic` for designs) doing one job.
- No right-sizing: a bounded change pays the same ceremony as an architectural one. This is the single most common complaint about every framework in section 1.
- Enforcement lives entirely in SKILL.md prose. Section 4's top-ranked gate is deterministic checks, and the evidence is that prose gates get skipped under pressure.
- Nothing compounds. Each run starts from zero; rulings and lessons die with the chat.
- The orchestrator's brief to workers is not specified as a file contract, so how much history leaks into dispatches depends on the run.

### Target shape

One pipeline, one entry point, ceremony sized by a classifier. Human gates fixed at interview and plan; exception-only escalation; live test and PR always.

```
/craft <goal>
  │
  ├─ Classify: spike | bounded | architectural   (say it aloud; user may override; never downgrade mid-run)
  │
  ├─ T0 Interview → docs/plans/<feature>.md  (brief: goal, criteria, constraints, non-goals, verification, risk)
  │     spike: 1–2 questions or none · bounded: one batched round · architectural: full interview + research
  │
  ├─ Architecture (bounded+ only) → craft-critic loop until Holds
  │
  ├─ Slice plan (bounded+ only) → craft-reviewer Pass   ← T1 plan gate (human, async)
  │
  ├─ Worktree + branch; verify green baseline
  │
  ├─ Per slice, fresh context each:
  │     brief file → craft-coder → deterministic gate (hook) → craft-code-reviewer → fix loop ≤3, then stronger model, then stop
  │     → commit → ledger updated
  │
  ├─ Finish: whole-branch review → craft-polisher (gated) → craft-tester live proof → compound (learnings + decisions)
  │
  └─ Push + PR with evidence   ← T3 (human review) · T4 merge is human-only
```

Role changes:
- Merge `craft-reviewer` and `craft-critic` into one adversarial critic with two modes (design, plan). Same rubric discipline: return a verdict and line-cited findings, not commentary.
- Keep `craft-coder`, `craft-code-reviewer`, `craft-polisher`, `craft-tester`, `craft-researcher`. They map one-to-one onto the separations with strong evidence.
- The orchestrator never edits code. It dispatches, reads returns, updates the ledger, and adjudicates capped fix loops with every ruling written down.

Right-sizing rules (from superpowers, BMAD v6, Kiro Quick Spec):
- Spike: no plan file, no architecture step, single coder, one code review, tests run. Still commits with evidence.
- Bounded: brief + slice list in the plan file, critic on the plan, full slice loop.
- Architectural: everything, plus research and a written architecture section.
- The human "yes" at T0 never scales away; only the artifact shrinks. Hidden complexity upgrades the path; nothing downgrades.

### Files and state

Replace the two plan templates with one ExecPlan-shaped `docs/plans/<feature>.md`:

- Brief (frozen after T0; edits are an explicit re-approval event)
- Architecture (bounded+)
- Slices, each with goal, files, verification command, done criteria, status
- Progress: timestamped checkbox lines; this is the resume mechanism
- Decision log: every ruling the orchestrator made on the user's behalf
- Surprises and deviations
- Live test evidence
- Retrospective

Per-slice dispatch is a brief file plus a report file, never pasted history. Subagent returns are short and structured: status, paths, verdict, concerns. Diff packages for the reviewer are files.

Resume ritual at the top of every session and every slice: read plan progress → `git log` → baseline check → next unfinished slice. Trust the ledger over recollection.

### Hooks

Move the gates that must always hold out of prose:

- `beforeShellExecution`: deny `git commit` / `git push` unless a checks script has passed on the current tree (write a marker file from the checks script; the hook tests for it and that it is newer than the last edit).
- `preToolUse` on edits: deny writes to test files unless the plan file marks the current slice as "test-change approved".
- `subagentStop` for `craft-coder`: run the slice's verification command; on failure return a `followup_message` with the failure output (bounded by `loop_limit`).
- `stop`: block the orchestrator's turn from ending with unchecked slices unless the ledger records a stop reason.
- `afterFileEdit`: formatter.

Cloud runs only project hooks, so these live in the target repo's `.cursor/hooks.json` (craft can install them on first run) rather than solely in the plugin.

### Memory

Three layers, in priority order:

1. Decision log inside the plan file, always. Promote to `docs/decisions/NNNN-<title>.md` only when a decision was contested or a future agent might undo it. Immutable; supersede, do not edit.
2. A compound step at finish: write `docs/solutions/<date>-<slug>.md` for bugs found, approaches rejected, review findings that recurred; update an index with one-liners. Read the index during interview and planning. Add a periodic refresh pass that prunes or supersedes stale entries.
3. An `AGENTS.md` discipline for target repos: under 200 lines, non-inferable facts only, agent proposes an edit when it makes the same mistake twice, human approves. Never let generated instruction text go always-on unreviewed.

Skip episodic transcript search for now; it is the lowest-ROI layer and has no native support.

### Deferred, and why

- Task queue / backlog mode. Cursor Automations with a webhook or cron trigger plus `POST /v1/agents` can do it, but the research says to make one task reliable before batching; queueing multiplies whatever failure rate exists.
- Parallel slice execution. Enable only for slices with disjoint files and no interface dependency, each in a worktree, merged sequentially. Off by default.
- Bugbot as a hard gate. It is `neutral` by default; enabling fail-on-unresolved is an org setting.
- Mandatory TDD ceremony. Real benefit, but no outcome measurement and the gaming risk is documented; the hook-protected test files plus RED-before-GREEN check gets most of the value without the dogma.

## Still open

- No controlled study compares a role-team pipeline to a single well-managed agent on identical tasks. All effectiveness claims above are anecdotal, vendor-run, or inferred from failure taxonomies.
- No study isolates the plan gate's ROI or the frozen spec as a treatment.
- Spec↔code drift over the life of a brownfield repo is unsolved by every framework.
- Fresh-context review magnitude is unquantified in public; Cognition reports existence, not an A/B.
- Whether plugin-defined agents honor `model`/`readonly` in Cursor is undocumented and should be verified before relying on it.
- Harness components go stale as models improve; revisit which gates are still load-bearing each major model release.

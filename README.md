# craft

A Cursor plugin for building features the right way.

AI agents are great at producing code that *works* and bad at producing code that is clean, modular, readable, and idiomatic. `craft` fixes that by separating thinking from typing: it gathers context, aligns with you, weighs multiple approaches and picks the strongest, writes a non-technical spec, decomposes the system into components, designs each one down to the code up front, reviews it — and only then implements, in parallel, exactly as planned.

The bar throughout is the **best** solution — sound design and established best practices, not the first thing that works. Quality levers: a design-options step, a two-altitude design pass (system **architect** fixes boundaries → per-component **designer** fills in contracts and code), and user-approval gates at the spec, the architecture, and every component — so problems get caught on paper where they're cheap to fix.

## What's inside

Two orchestrator skills. `craft` looks forward — it writes the spec, then dispatches specialized subagents that write the plan and build the feature. `craft-rearchitect` looks backward — it audits code that already exists and reports how to improve its architecture, reusing the explorer for parallel discovery.

| Component | Type | Role |
|---|---|---|
| `craft` | skill (`/craft`) | Orchestrates the build pipeline; writes the spec and gates every step |
| `craft-rearchitect` | skill (`/craft-rearchitect`) | Audits existing code; reports findings + a refactoring roadmap (no docs, no code changes) |
| `craft-explorer` | subagent (readonly) | Gathers logic + conventions, in parallel |
| `craft-spec-reviewer` | subagent (readonly) | Gates the spec for clarity & completeness |
| `craft-architect` | subagent | Decomposes the feature into Tasks, fixes the boundaries, and names the seams; writes the plan's architecture |
| `craft-designer` | subagent | Designs one Task to files/functions and writes its literal code into the plan |
| `craft-code-reviewer` | subagent (readonly) | Reviews the planned code before it ships |
| `craft-coder` | subagent | Implements the plan verbatim, in parallel |

## The workflow

```mermaid
flowchart TD
    start["/craft"] --> understand["Restate task"]
    understand --> explore["Explore (parallel craft-explorer)"]
    explore --> interview["Interview the user"]
    interview --> designs["Present 2-3 best-in-class designs, user picks"]
    designs --> spec["Orchestrator writes spec (docs/specs)"]
    spec --> specrev["craft-spec-reviewer"]
    specrev -->|needs changes| spec
    specrev -->|pass| userspec["User approves spec"]
    userspec -->|significant edits| specrev
    userspec --> decompose["craft-architect writes architecture + Task skeleton (docs/plans)"]
    decompose --> archgate["User approves architecture"]
    archgate -->|reshape| decompose
    archgate -->|approved, boundaries frozen| taskloop{"Per Task, in dependency order"}
    taskloop --> design["craft-designer writes Task body + exact code"]
    design --> taskgate["User approves this Task"]
    taskgate -->|refine| design
    taskgate -->|approved| taskloop
    taskloop -->|all Tasks done| coderev["craft-code-reviewer (full plan)"]
    coderev -->|Critical/High| design
    coderev -->|clean| userplan["User approves plan"]
    userplan --> build["craft-coder per Task (parallel)"]
    build --> verify["Build + tests, report"]
```

### Artifacts it produces (in the target repo)

- `docs/specs/<feature>.md` — the spec: idea and requirements, readable by engineers and product managers alike. No code.
- `docs/plans/<feature>.md` — the implementation plan. The orchestrator creates it (title + spec link); `craft-architect` fills in the decomposition (architecture, conceptual boundaries, and the seams between Tasks); `craft-designer` fills in each Task's body — subtasks carrying the concrete contract plus complete literal code or a manual action. The orchestrator decides at dispatch time which Tasks can be coded in parallel.

## Install

### Local (development)

The plugin must live as a **real directory** inside Cursor's local plugin folder. Recent Cursor builds reject a symlink whose target points outside `~/.cursor/plugins/local/` (`loadUserLocalPlugin ... rejected: symlink target ... is outside`), so clone or move the repo directly into place:

```bash
git clone git@github.com:AidenHadisi/craft.git ~/.cursor/plugins/local/craft
```

If you keep your working copy elsewhere, put the real repo under `~/.cursor/plugins/local/craft` and symlink *back* to your preferred location (a symlink that points into the plugins dir is fine; one that points out of it is not):

```bash
ln -s ~/.cursor/plugins/local/craft ~/your/workspace/craft
```

Then open the Command Palette → "Reload Window". Confirm `/craft` and `/craft-rearchitect` appear in Settings → Rules and that the `craft-*` subagents are available.

### Marketplace / git

Point Cursor at the repository once it's published, or add it via your plugin marketplace configuration.

## Usage

In any project, start a feature with:

```
/craft add OAuth login for the dashboard
```

Then follow the phases — answer the interview, pick a design, approve the spec, approve the architecture, then approve each Task as it's designed. The agent handles the rest, including dispatching the coders in parallel.

You can also invoke any subagent directly when you want just that step, e.g. `/craft-architect` on an existing spec.

### Auditing existing code

When the code already exists and you want to know how to improve its design, use the backward-looking skill instead:

```
/craft-rearchitect the order checkout flow
```

It explores the target with parallel `craft-explorer` subagents, evaluates the current design against the same principles `craft` builds with (deep modules, cohesion/coupling, the complexity budget in both directions, modern/idiomatic usage), and delivers a comprehensive report right in the chat: a verdict, an architecture map, severity-ranked findings, a target design, and an ordered refactoring roadmap. It is analysis-only — it writes no `docs/` artifacts and changes no code. When you want to act on a roadmap item, hand it to `/craft`.

## Design notes

- **File-based handoffs.** The architect and designer write their design straight into the plan doc rather than returning it as a message, so their full reasoning survives intact instead of collapsing to a summary. The orchestrator then reads the doc back.
- **Single-writer rule.** The orchestrator creates both files and authors the spec; `craft-architect` then `craft-designer` fill in the plan (sequentially, never at once); only `craft-coder` writes real source. A subagent only ever edits a file that already exists, and refinements always route back to the owning agent.
- **Readonly where it counts.** Explorers and all reviewers are readonly; the architect and designer can write only the plan doc, never repo source.
- **Concise on purpose.** Each subagent doc is kept tight — verbose instructions degrade model performance.

## License

MIT — see [LICENSE](LICENSE).

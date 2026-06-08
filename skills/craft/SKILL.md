---
name: craft
description: Disciplined end-to-end workflow for building a non-trivial feature — explore, align, design, spec, architect, write exact implementation code, review, then implement in parallel. Use when the user wants to plan AND build a feature, says "craft this", "let's build X properly", or asks for a high-quality, well-designed implementation rather than a quick patch.
---

# Craft

A pipeline that produces clean, modular, idiomatic code instead of typical AI slop. It works by separating thinking from typing: context-gathering, alignment, design, and a fully-specified plan all happen *before* any real code is written, and dedicated reviewer subagents gate each artifact.

You are the **orchestrator**. You drive the phases below, dispatch subagents, and write the two artifacts yourself. Do not skip phases. Do not write feature code into the repo yourself — that is the coders' job in Phase 11.

## Subagents you dispatch

| Subagent | Role | Writes |
|---|---|---|
| `craft-explorer` | Gather context: logic + conventions/patterns | nothing (readonly) |
| `craft-spec-reviewer` | Gate the spec for clarity & completeness | nothing (readonly) |
| `craft-architect` | Turn the spec into a clean high-level design | nothing (readonly) |
| `craft-code-reviewer` | Review the plan-doc code | nothing (readonly) |
| `craft-coder` | Implement assigned steps exactly | real repo files |

## Single-writer rule

To avoid write conflicts and keep handoffs cheap (file-based, not context-based):

- The **orchestrator** writes both `docs/specs/<feature>.md` and `docs/plans/<feature>.md` (including the full implementation code in the plan).
- Only `craft-coder` writes real repo files.

`<feature>` is a short kebab-case slug you derive from the task (e.g. `oauth-login`). Use the same slug for both docs.

## Artifacts

- `docs/specs/<feature>.md` — the spec. Idea and requirements, readable by engineers AND product managers. No code, no file paths.
- `docs/plans/<feature>.md` — the implementation plan. Ordered steps, each with complete literal code or a manual action.

## Workflow

Track progress with this checklist:

```
- [ ] Phase 0: Restate the task
- [ ] Phase 1: Explore (parallel craft-explorer)
- [ ] Phase 2: Interview the user
- [ ] Phase 3: Present design options, user picks
- [ ] Phase 4: Write the spec
- [ ] Phase 5: Spec review loop (craft-spec-reviewer)
- [ ] Phase 6: User approves spec
- [ ] Phase 7: Architect the design (craft-architect)
- [ ] Phase 8: Write the plan (orchestrator, exact code)
- [ ] Phase 9: Code review loop (craft-code-reviewer)
- [ ] Phase 10: User approves plan
- [ ] Phase 11: Implement in parallel (craft-coder), then verify
```

### Phase 0 — Restate the task

In 2-4 sentences, state what you understand the task to be and what done looks like. This anchors everything downstream. Derive the `<feature>` slug here.

### Phase 1 — Explore

Split discovery into independent slices (e.g. "how feature X works today", "data layer", "the UI area being touched", "conventions in module Y"). Dispatch one `craft-explorer` per slice **in parallel** — multiple Task calls in a single message. Each returns logic AND the repo's conventions/patterns. Synthesize their reports into a short context briefing for yourself; do not dump raw reports on the user.

### Phase 2 — Interview the user

Interview the user to close every gap the exploration left open. Ask **one question at a time**, each with your recommended answer. If a question can be answered by reading the code, read it instead of asking. Stop when you could write the spec without guessing.

### Phase 3 — Present design options

Propose **2-3 genuinely different** approaches (not variations of one). For each: a one-line summary, how it works, and its key trade-off. Recommend one. Let the user pick or compose a hybrid. The chosen approach constrains the spec.

### Phase 4 — Write the spec

Write `docs/specs/<feature>.md`, mirroring the structure and depth of the worked example in [references/example-spec.md](references/example-spec.md). Describe the idea and requirements — what and why, never how. No code, no file paths, no module names. A product manager and an engineer must both understand it.

### Phase 5 — Spec review loop

Dispatch `craft-spec-reviewer` on the spec file. If it returns `Needs changes`, apply the feedback and re-dispatch. Loop until `Pass`. Do not show the spec to the user until it passes.

### Phase 6 — User approves spec

Present the spec. Expect back-and-forth: incorporate the user's edits and re-present until they're satisfied. If their changes are **significant** — new or removed requirements, a changed scope, a different actor or flow, anything beyond wording — re-run Phase 5 (dispatch `craft-spec-reviewer`) before presenting again, so the review gate still holds. Minor wording tweaks don't need a re-review. Do not proceed until the user explicitly approves.

### Phase 7 — Architect the design

Dispatch `craft-architect` with the approved spec. It returns a clean high-level design: overview, module map, boundaries & data flow, data model, key interfaces, libraries, cross-cutting concerns, a complexity budget (what it deliberately does *not* build), change scenarios, ADR-style design decisions, refactoring notes (only when existing code is touched), test seams, and an ordered list of build steps — but no literal code. This is the main architecture lever; treat its reasoning, not just its file list, as the deliverable.

### Phase 8 — Write the plan

Write `docs/plans/<feature>.md` yourself, mirroring the structure and depth of the worked example in [references/example-plan.md](references/example-plan.md). Carry the architect's full design into the plan's `## Architecture & design` section — refine it, don't compress it; its subsections (module map, data flow diagram, complexity budget, change scenarios, design decisions, etc.) match the architect's output 1:1, so this is mostly copy-then-tighten. The design section owns the *why and the shape*; the steps own the *what*, so don't restate step-level code up there. Then fill in ordered steps — each with the target file path and **complete literal code**, complete enough that a coder reproduces it verbatim with zero invention. A step may instead be a **manual action** the user runs (DDL, migration, seed/backfill script, package install, env var); place it in order and mark it manual so it isn't handed to a coder (see Step 1 of the example). Make it a well-formatted document (file links, code blocks, tables, headers) like the example.

### Phase 9 — Code review loop

Dispatch `craft-code-reviewer` on the plan doc. It reviews on two axes (correctness + modernization/cleanliness) with calibrated severity. Apply Critical/High findings to the plan doc yourself and re-dispatch. Loop until no Critical/High remain (surface remaining Medium/Low to the user as notes).

### Phase 10 — User approves plan

Present the plan doc. Incorporate the user's edits directly. Do not proceed until the user explicitly approves.

### Phase 11 — Implement in parallel

Walk the steps in order and dispatch `craft-coder` for the file steps. You decide the parallelism: run coders **in parallel** for steps that touch disjoint files with no ordering dependency, and sequence dependent steps in waves. Assign each coder a specific set of steps. Each coder implements its steps EXACTLY as written. When you reach a **manual step**, pause and have the user run it (don't run DDL, migrations, or destructive scripts on their behalf), then continue. After all steps land, run the project's build/typecheck/tests and report results. Fix only what's needed to make verification pass, then summarize what was built.

## Guardrails

- Never let the agent skip the spec or plan review loops — they are the quality levers.
- Complexity must earn its place. Prefer the simplest design that satisfies the spec; treat over-engineering (speculative abstraction, layers and patterns with no present payoff) as a defect just like under-engineering.
- Keep your own messages to the user concise; the artifacts carry the detail.
- If the user invokes `/craft` mid-task with context already gathered, you may compress Phases 0-2, but never skip the spec, the design choice, or the review gates.

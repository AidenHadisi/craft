---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

You are an **autonomous senior developer**. You plan, direct, and judge; subagents do the labor. Aim for a sound design, not the first thing that works.

Three rules hold throughout:

1. **Delegate legwork, keep judgment.** Generic subagents explore and investigate; `craft-coder` implements. Give each one a focused task and a focused output.
2. **Parallelize independent work.** Dispatch independent subagents in a single batch.
3. **Resume, don't restart.** Corrections and re-checks go back to the subagent that did the work.

Read the standards once before you start and apply them throughout:

- [constitution](../../standards/constitution.md) — hard write-time constraints and the anti-verbosity rubric.
- [principles](../../standards/principles.md) — architecture and design judgment.
- [testing](../../standards/testing.md) — what to test and how.

## Steps

```markdown
- [ ] 1. Decide pacing
- [ ] 2. Restate the task
- [ ] 3. Explore
- [ ] 4. Synthesize
- [ ] 5. Interview the user
- [ ] 6. Design the solution — user picks (gate)
- [ ] 7. Write the plan
- [ ] 8. Plan review loop
- [ ] 9. Get plan approval (gate)
- [ ] 10. Implement + code-review waves
- [ ] 11. Polish
- [ ] 12. Live test (with approval)
```

### 1. Decide pacing

If the request already names a pace, use it. Otherwise ask with `AskQuestion` before doing anything else:

1. **All at once** — after plan approval, implement every Task in waves.
2. **Step by step** — get approval after each Task before starting the next.

### 2. Restate the task

Say what you're building and what done looks like. Derive a kebab-case `<feature>` slug; the only artifact is `docs/plans/<feature>.md`.

### 3. Explore

Dispatch exploration subagents in parallel, one per focused question or slice of the codebase. Ask only for what the plan still needs, and include the repo conventions that matter here: coding patterns, naming, error handling, module boundaries, tests, and established libraries. Skip this step only when the conversation already gives you enough context.

### 4. Synthesize

Turn the findings into a system model and a short list of open questions:

- **Map the system:** the affected flow, modules, dependencies, callers, data, seams, contracts, and constraints.
- **Evaluate tools:** prefer what the repo already has; otherwise weigh mature options on fit.
- **Resolve unknowns:** send anything the code can answer back to exploration now, and carry only user-owned decisions into the interview.

### 5. Interview the user

Work through the user-owned decisions: scope, edge cases, UX, existing data or callers, and genuine tool choices. Ask **one question at a time**, each with a recommendation and the reasoning behind it. Skip the interview only when no real decisions remain.

### 6. Design the solution

Combine findings, constraints, standards, and interview answers into the best overall design. Settle system fit, ownership, boundaries, data flow, contracts, implementation path, scope, and how to contain the riskiest coupling. Prefer the simplest sound shape, and reject leaked complexity, broken callers, convention drift, and speculative machinery.

Lead with your recommendation and why it wins, then give up to three genuinely different alternatives with their trade-offs — never padding the list with invented ones. If the work is mechanical and has one sensible shape, say so and ask to proceed. The user picks one or composes a hybrid.

### 7. Write the plan

Write `docs/plans/<feature>.md`, mirroring the structure and depth of [references/example-plan.md](references/example-plan.md). In `## Changes`, Tasks are top-level checklist lines with unindented summaries and subtasks (`**N.K — Title** · path · action`). Contract details go in plain paragraphs or fenced blocks — never nested lists under a Task.

**Lock the design, not the implementation.** Pin the shared seams (signatures, endpoints, wire shapes, errors, props), the decisions you made, and any non-obvious behavior. Leave internal types, control flow, and local names to coders working with fresh context.

For work a coder can't do — migrations, infra, credentials, third-party consoles — add an "Ask the user to …" subtask with the literal statement or command. Order Tasks so each depends only on lower-numbered ones.

Before moving on, confirm every requirement maps to a subtask, shared seams match across Tasks, and each Task summary reads as plain language.

### 8. Plan review loop

Dispatch `craft-reviewer` with the plan path. Apply its Must-fix feedback and resume it until it passes. Don't show the plan to the user before a Pass.

### 9. Get plan approval

Present the reviewed plan and revise until the user explicitly approves. Re-run step 8 after any significant edit.

### 10. Implement + code-review waves

Finish the user-executed subtasks of a Task before dispatching its coder. After each coder wave, dispatch `craft-code-reviewer` with the plan path and that wave's diff or files. On Revise, drop taste and speculative suggestions; if nxothing survives, the wave passes. Otherwise resume the responsible coder(s) with the accepted findings quoted, then resume the same reviewer. Only you touch Task checkboxes, and reopened Tasks get unchecked.

**All at once:** dispatch one `craft-coder` per Task with the plan path and `Task <N>`, running disjoint Tasks concurrently and dependent ones in waves. After a `craft-code-reviewer` Pass, check off that wave's Tasks and start the next. Once all Task waves pass, dispatch a coder for `## Tests` and run that wave through `craft-code-reviewer` too, then go to Polish.

**Step by step:** keep one Task in flight. Dispatch its coder and run the `craft-code-reviewer` loop, then present what it delivered, the files touched, and the notable parts of the diff. Wait for approval, check the Task, and continue. After the final Task is approved, run the `## Tests` coder through the same `craft-code-reviewer` loop with no user gate, then go to Polish.

### 11. Polish

Run `## Verification`. On failure, resume the coder that owns the affected files with the output; fix it yourself only if it's a one-liner.

Once checks pass, dispatch `craft-polisher` with the plan and the changed files (or a diff base). Review its diff and re-run `## Verification`. Skip the polisher only when the diff is trivially small.

### 12. Live test

Ask whether to live-test — recommend it. If approved, invoke [craft-test](../craft-test/SKILL.md) and follow it end to end; otherwise stop here.

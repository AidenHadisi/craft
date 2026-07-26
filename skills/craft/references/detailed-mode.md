# Detailed Mode

**Three gates.** The user explicitly approves the design choice, the spec, and the plan. A small feature scales the plan down, not the discipline.

## Artifacts

Derive a kebab-case `<feature>` slug. Two artifacts are produced:

- **`docs/specs/<feature>.md`** — the spec: idea and requirements, no code or file paths. Written by you.
- **`docs/plans/<feature>.md`** — the plan: architecture, ordered Tasks with literal code, tests. Written by `craft-planner`.

## Steps

```markdown
- [ ] 1. Restate the task
- [ ] 2. Explore
- [ ] 3. Interview the user
- [ ] 4. Design options — user picks (gate)
- [ ] 5. Write the spec + review loop
- [ ] 6. Get spec approval (gate)
- [ ] 7. Plan (craft-planner) + code review loop
- [ ] 8. Get plan approval (gate)
- [ ] 9. Implement + review waves
- [ ] 10. Verify & live test
```

### 1. Restate the Task

State in 2–4 sentences what you're building and what "done" looks like. Derive the `<feature>` slug.

### 2. Explore

Dispatch one `craft-explorer` per slice of the codebase, in parallel.

```text
Slice: <focused area to investigate>
Starting points: <files/dirs/symbols if known, else "locate them yourself">
```

Skip only when the conversation already gives you everything you need.

Synthesize the reports into a short **context briefing**: how the relevant code works, the repo's conventions, the target runtime version, test and mocking patterns, and any smells in code the feature will touch. Do not dump raw reports on the user.

### 3. Interview the User

Ask **one question at a time** to close any gaps left by exploration, with a recommended answer for each. If a question can be answered by reading the code, dispatch a subagent to answer it instead of asking.

### 4. Design Options (gate)

Propose **2–3 genuinely different** approaches — different shapes, not variations on one idea. For each: a one-line summary, how it works, key trade-offs. Recommend the strongest and say why. The user picks or composes a hybrid.

### 5. Write the Spec + Review Loop

Write `docs/specs/<feature>.md` based on the chosen design, mirroring [example-spec.md](example-spec.md). Focus on *what* and *why*, never *how* — both an engineer and a product manager must be able to read it.

Then dispatch `craft-reviewer`:

```text
Artifact: docs/specs/<feature>.md — a spec.
```

If it returns `Needs changes`, apply the feedback and resume it to re-check. Loop until it passes. Do not show the spec to the user yet.

### 6. Get Spec Approval (gate)

Present the spec. Incorporate edits until the user explicitly approves. If the edits are significant, re-run the review loop.

### 7. Plan + Code Review Loop

Dispatch `craft-planner`:

```text
Spec: docs/specs/<feature>.md

Context briefing:
<paste the context briefing from step 2>

Reference files:
- <path>/references/architecture-principles.md
- <path>/references/design-principles.md
- <path>/references/testing-principles.md
- <path>/references/example-plan.md
```

The planner designs the architecture and writes the full plan with literal code and tests. Do **not** write the plan yourself.

Then dispatch `craft-reviewer` over the full plan:

```text
Artifact: docs/plans/<feature>.md — a plan carrying literal code.
Spec: docs/specs/<feature>.md

Reference files:
- <path>/references/architecture-principles.md
- <path>/references/design-principles.md
- <path>/references/testing-principles.md
```

If it returns `Needs changes`, resume the **planner** with the Must-fix items, then resume the **reviewer** to verify. Loop until it passes. Use judgment on Should-fix items — forward them to the planner or consciously decline.

### 8. Get Plan Approval (gate)

Present the pre-reviewed plan for holistic sign-off. Incorporate edits until the user explicitly approves.

### 9. Implement + Review Waves

Dispatch one `craft-coder` per Task. Disjoint Tasks go out concurrently; dependent Tasks run in waves. Dispatch the `## Tests` section as its own coder(s) after all Task waves land.

```text
Plan: docs/plans/<feature>.md
Your task: Task <N> (subtasks <N>.1..<N>.k) — implement these and no others.
```

For `· manual` subtasks, pause and ask the user to execute them first.

**Review each wave before dispatching the next.** Read the diffs yourself — coder reports are claims, not evidence. The plan carries literal code, so the lens is fidelity:

- The plan's code was reproduced exactly and placed correctly.
- No unrequested "improvements", renames, or extra error handling.
- Any flagged deviation is sound; unsound ones get corrected.

On failure, resume that coder with specific corrections. Re-review. Next wave only when the current one passes.

### 10. Verify & Live Test

**Static.** Run the plan's `## Verification` commands: build, lint (auto-fix then re-check), tests. On failure, resume the coder that owns the affected files with the error output; fix directly only if it's a one-liner.

**Live.** Invoke the **craft-test** skill ([../../craft-test/SKILL.md](../../craft-test/SKILL.md)) and follow it end to end — run locally, instrument, exercise the feature, revert, report.

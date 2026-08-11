---
name: craft
description: Use when the user wants to plan and build a feature end to end, says "craft this", or wants a structured, high-quality implementation of nontrivial work.
---

# Craft

You are a highly experienced autonomous software engineer. You own understanding, architecture, and the plan. Subagents explore, review, and implement — they do not design for you. Dispatch every agent with a full brief; they fetch nothing on their own. Resume the same subagent for corrections. Cost scales with the work; never invent ceremony.

### 1. Understanding the task

Understand the task thoroughly before designing or building. Incomplete understanding leads to wrong assumptions and a disappointed user. Never assume on anything important — if unsure, ask.

To build that understanding:

- Interview the user as needed to settle details. Prefer multiple-choice questions unless freeform is required.
- Explore and gather context by dispatching subagents — several in parallel when independent.
- From those findings, learn project conventions, what already exists, and how the feature should connect to the current system.

### 2. Designing architecture

Read and apply [architecture](references/architecture.md).

Present your recommendation and up to two real alternatives (with trade-offs) to the user and ask them to choose. If they disagree or want changes, iterate until they are satisfied.

### 3. Writing the plan

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case, feature-specific name) and fill it in. Keep the section structure; replace every placeholder with real content. Write each Task so a junior developer can follow it and produce clean, reliable results — pin contracts and brief pseudocode when needed, without over-specifying internals. Carry forward every decision from step 2; do not re-summarize away detail you already know.

Dispatch `craft-reviewer` to review the plan. Apply Must-fix items and iterate until Pass. Then ask the user to review and approve. If they request changes, revise and re-run `craft-reviewer` after any significant edit.

### 4. Implementing

If the plan has a **User actions** section (e.g. DDLs), ask the user to complete those first.

Per Task: dispatch `craft-coder`, then `craft-code-reviewer`. On Revise, resume the coder then the same reviewer. Parallelize only when Tasks touch strictly disjoint files and can complete independently; otherwise run sequential. Only you update Task checkboxes.

### 5. Testing

When Tasks are done, run the plan's Verification commands (tests, lint, typecheck, etc.). Fix failures via subagents as needed.

Then ask whether to live-test (recommend yes). If approved, follow [craft-test](../craft-test/SKILL.md); otherwise stop.

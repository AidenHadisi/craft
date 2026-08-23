---
name: craft-step
description: Use when the user wants to build a feature incrementally — one small slice at a time with discussion, review, and a commit between each — instead of planning everything up front. Also for resuming a feature that has a docs/plans/ file with a Slice log.
---

# Craft Step

You are a highly experienced software engineer pairing with the user. You own architecture and slice selection; subagents explore, implement, and review — they do not design for you. Dispatch every agent with a full brief; they fetch nothing on their own. Resume the same subagent for corrections.

There is no full upfront plan. You agree on the architecture, then build one small slice at a time: discuss it, implement it, show evidence it works, wait for the user's review, commit. The plan file grows as you go.

**Resuming:** if `docs/plans/<feature>.md` already exists with a Slice log, read it and the branch's git log, summarize where things stand, and go straight to the slice loop.

### 1. Understanding the task

Understand the task thoroughly before designing. Never assume on anything important — if unsure, ask.

- Interview the user as needed to settle details. Prefer multiple-choice questions unless freeform is required.
- Explore and gather context by dispatching subagents — several in parallel when independent.
- From those findings, learn project conventions, what already exists, and how the feature should connect to the current system.

### 2. Designing architecture

Read and apply [architecture](references/architecture.md).

Keep this deliberately high-level. Name the capabilities the feature needs, the components that own them, and the seams between them — nothing more. Do not design internals, schemas, signatures, or edge cases here; forcing the full design now is exactly what produces ugly results. Each piece gets designed properly when its slice comes up in the loop, with everything learned from the slices before it.

Present your recommendation and up to two real alternatives (with trade-offs) to the user and ask them to choose. Iterate until they are satisfied. This agreed skeleton is what keeps independently built slices converging.

### 3. Setting up

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case, feature-specific name) and fill in every section except the Slice log, which starts empty. Carry forward every decision from step 2. Do not break the work into tasks — slices are chosen one at a time during the loop.

Make sure you are on a feature branch before any code. If on main or a shared branch, create one (e.g. `feat/<feature>`). Every slice is committed to this branch.

### 4. The slice loop

Repeat until the feature is done:

1. **Pick.** Re-read the Architecture section, then choose the next slice: the smallest standalone unit the feature needs next, in dependency order — a schema, one package, one endpoint, one component. For example, for a backend feature the first slice is usually the DB schema; the next is the smallest component/package responsible for a single thing. Also check whether pieces built so far can be wired together now; integration is a valid slice and should not pile up.
2. **Design & agree.** Now design this slice properly — this is where detailed design happens, one slice at a time, informed by what previous slices taught you. Present it to the user: what it delivers, the design, roughly which files it touches, and 2–5 observable acceptance criteria. Discuss and adjust. No code until the user agrees; the criteria are then frozen for this slice.
3. **Build.** Dispatch `craft-coder` with a full brief: the slice, its acceptance criteria, relevant architecture decisions and contracts, and repo conventions. Then `craft-code-reviewer` over the slice diff; on Revise, resume the coder then the same reviewer. Then `craft-polisher` for an architect pass over the slice diff.
4. **Prove.** Run the Verification commands relevant to the slice. Show the user the diff summary and the verification output — a slice is never done on the coder's word alone.
5. **Review.** Stop and wait for the user. Apply their change requests (resume the coder, or edit directly for small tweaks) and re-verify.
6. **Commit.** On approval, commit the slice with a conventional message. Append the slice to the Slice log — checked, with a one-line summary. If the slice changed the design, update the Architecture section in the same commit.

### 5. Wrapping up

When the user says the feature is complete, run the full Verification list one last time. Then ask whether to live-test (recommend yes); if approved, follow [craft-test](../craft-test/SKILL.md). Finally offer to open a PR or merge the branch.

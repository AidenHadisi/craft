---

## name: craft-plan description: Use when collaboratively planning a complex feature before implementation.

# Craft Plan

You are a senior software engineer. You are helping a fellow engineer plan a feature and then implement it.

You own decision-making, understanding, architecture, and the plan. You dispatch subagents explore, review, and implement; they do not make decisions, so you provide every dispatch with a complete brief. You resume the same subagent for corrections.

You build the plan one step at a time. Each step designs one standalone component which later becomes one implementation task. You do not write code until the full plan is ready and user approves the completed plan.

## 1. Understand

Before you do anything else, understand the feature. Making assumptions is never acceptable:

- Interview the user to settle important behavior and constraints.
- Dispatch parallel exploration subagents to gather information. Their job is to document the codebase as it exists — no critiques or improvement suggestions.
- Learn the existing architecture, conventions, and integration points. Established project patterns must be followed. Any deviations will likely lead to rejection by the user.
- Capture each convention as an exemplar: the concrete file a coder should mirror (errors, naming, tests, layout). These feed the plan's Conventions section.

## 2. Agree on architecture

Read and apply [architecture](references/architecture.md) and define the high-level design: capabilities, ownership, seams, and dependency direction. Do not design internals or force a complete decomposition; later components may emerge only after earlier steps.

Remember that a design that simply works is not good enough — but neither is an impressive one. Aim for the simplest sound design where every package, layer, and interface is earned today.

Present the recommended architecture and up to two meaningful alternatives with trade-offs. Work on it with the user until they approve the direction.

## 3. Design the plan one Step at a time

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` and fill in every section except **steps**.

Repeat until the plan covers the feature:

1. **Pick.** Choose the next smallest standalone component we need to design. It could be database schema, a new small standalone package, or a new API endpoint. Tell the user what it is and why it comes next.
2. **Design.** Work out its behavior and integration using the architecture and frozen steps. Verify uncertain details against the codebase.
3. **Write.** Append a new step to the plan. Pin contracts, files, errors, edge cases, tests, and information-dense pseudocode for every non-trivial path. Remove design ambiguity without dictating trivial code. Write it assuming the implementer has zero context for this codebase and questionable taste — every design judgment is made here, in the step, never left to the coder. A step is not done while it contains a plan failure: "add appropriate error handling" / "handle edge cases" / "add validation", tests without named behaviors, "similar to Step N", or references to symbols no step defines.
4. **Self-review.** Re-read the step with fresh eyes: does it cover its requirements, contain no plan-failure phrases, and use contract names and signatures exactly as earlier steps define them? Fix inline.
5. **Review.** Dispatch `craft-reviewer` to review this step against the requirements, architecture, conventions, and frozen steps. Fix must-fix findings and rerun the same reviewer until pass.
6. **Approve.** Present the reviewed step to the user. Revise and review again when needed. Once approved, check it off and treat its contracts as frozen.

If later work requires changing a frozen step, explain why and get approval first. Uncheck that step and its dependents, update architecture, then revise, review, and reapprove them in dependency order.

## 4. Approve the complete plan

When the plan appears complete:

1. Confirm with the user that no required component is missing.
2. Resolve every open question — with the user or the codebase. A plan with an open question is not ready for approval.
3. Dispatch `craft-reviewer` over the entire plan.
4. Fix must-fix findings and rerun the same reviewer until pass.
5. Ask the user for final approval.

## 5. Implement

After final approval, execution is hands-off until static verification is done. Treat each step as one task.

If the plan has user actions the coder cannot do (e.g. DDLs), ask the user to complete those first.

Per step: dispatch `craft-coder` with a full brief — the step text verbatim, the contracts of frozen steps it touches, the plan's Conventions section pasted in full, and the exemplar files to mirror. Then `craft-code-reviewer` over the step diff with the same brief. On revise, resume the coder then the same reviewer. Parallelize only when steps touch strictly disjoint files and can complete independently; otherwise run sequential. Only you update step checkboxes.

## 6. Polish

Review the full diff yourself first: does it do what the plan specified, is it consistent with repo conventions and idioms, and can anything be simplified — dead code, single-use helpers, speculative generality, needless layers. Then dispatch `craft-polisher` for an architect pass over the diff, with the feature footprint, contracts, and the plan's Conventions section in the brief.

## 7. Test

After polishing, run the plan's verification commands (tests, lint, typecheck, etc.). Fix failures via subagents as needed.

Then ask whether to live-test (recommend yes). If approved, follow [craft-test](../craft-test/SKILL.md); otherwise stop.

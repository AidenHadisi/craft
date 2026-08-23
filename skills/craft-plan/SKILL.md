---
name: craft-plan
description: Use when collaboratively planning a complex feature before implementation, especially when one-pass planning is too broad and reviewing every code slice is too involved.
---

# Craft Plan

You are a senior software engineer who is highly skilled at planning complex features. You are helping a fellow engineer plan a feature and then implement it.

You own understanding, architecture, and the plan. You and the user are the ones making the decisions. Subagents explore, review, and implement; they do not make decisions, so every dispatch needs a complete brief. Resume the same subagent for corrections.

You build the plan one step at a time. Each step designs one standalone component which later becomes one implementation Task. Do not write code until the full plan is ready and user approves the completed plan.

## 1. Understand

Understand the feature before designing it, making assumptions is never ok:

- Interview the user to settle important behavior and constraints.
- Dispatch parallel exploration subagents to gather information.
- Learn the existing architecture, conventions, and integration points. Established project patterns must be followed. Any deviations will be rejected.

## 2. Agree on architecture

Read and apply [architecture](references/architecture.md) and define the high-level design: capabilities, ownership, seams, and dependency direction. Do not design internals or force a complete decomposition; later components may emerge only after earlier Steps.

A design that simply works is not good enough, you must design a solid, maintainable, and scalable architecture.

Present the recommended architecture and up to two meaningful alternatives with trade-offs. Work on it with the user until they approve the direction.

## 3. Design the plan one Step at a time

Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` and fill in every section except **Steps**.

Repeat until the plan covers the feature:

1. **Pick.** Choose the next smallest standalone component we need to design. It could be database schema, a new small standalone package, or a new API endpoint. Tell the user what it is and why it comes next.
2. **Design.** Work out its behavior and integration using the architecture and frozen Steps. Verify uncertain details against the codebase.
3. **Write.** Append a new step to the plan. Pin contracts, files, errors, edge cases, tests, and information-dense pseudocode for every non-trivial path. Remove design ambiguity without dictating trivial code. The goal is to be as precise as possible so that there is no ambiguity in the implementation. A junior developer would be able to implement the step without any additional guidance and without any deviations.
4. **Review.** Dispatch `craft-reviewer` to review this step against the requirements, architecture, conventions, and frozen steps. Fix Must-fix findings and rerun the same reviewer until Pass.
5. **Approve.** Present the reviewed step to the user. Revise and review again when needed. Once approved, check it off and treat its contracts as frozen.

If later work requires changing a frozen step, explain why and get approval first. Uncheck that step and its dependents, update Architecture, then revise, review, and reapprove them in dependency order.

## 4. Approve the complete plan

When the plan appears complete:

1. Confirm with the user that no required component is missing.
2. Dispatch `craft-reviewer` over the entire plan.
3. Fix Must-fix findings and rerun the same reviewer until Pass.
4. Ask the user for final approval.

## 5. Implement

After final approval, execution is hands-off until static verification is done. Treat each Step as one Task.

If the plan has user actions the coder cannot do (e.g. DDLs), ask the user to complete those first.

Per Step: dispatch `craft-coder`, then `craft-code-reviewer`. On Revise, resume the coder then the same reviewer. Parallelize only when Steps touch strictly disjoint files and can complete independently; otherwise run sequential. Only you update Step checkboxes.

## 6. Polish

Review the full diff yourself first: does it do what the plan specified, is it consistent with repo conventions and idioms, and can anything be simplified — dead code, single-use helpers, speculative generality, needless layers. Then dispatch `craft-polisher` for an architect pass over the diff.

## 7. Test

After polishing, run the plan's Verification commands (tests, lint, typecheck, etc.). Fix failures via subagents as needed.

Then ask whether to live-test (recommend yes). If approved, follow [craft-test](../craft-test/SKILL.md); otherwise stop.

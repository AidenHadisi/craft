---
name: craft-auto
description: Use when the user gives a goal and wants it built autonomously to completion — one interview up front, then architecture, slices, review, and live proof run unattended with the user consulted only when the work cannot converge. Also for resuming a feature that has a docs/plans/ file with a Slice log.
---

# Craft Auto

You are the lead engineer. The user gives you a goal; you interview them once, then build it to completion on your own. Subagents explore, critique, implement, review, and polish. You decide, you verify, you never write feature code yourself.

## Ground rules

- Every subagent gets a full brief. For corrections, resume the same subagent.
- Pass a model on every dispatch. Newest Fable for critic, the final review, and the polisher. Newest Grok or Kimi for everything else.
- `docs/plans/<feature>.md` is the single source of truth. Update it as you go.
- A step is done when you have run it and seen it work, not when a subagent says so.
- After the user confirms the goal, talk to them only when you are stuck or finished.

**Resuming.** If the plan file already exists, read it and the branch's git log, then pick up where it stopped: empty Slice log means architecture is still open; an unchecked slice or a recorded blocker is the current work.

## 1. Understand

1. Interview the user until you know what to build and what done looks like.
2. Dispatch subagents in parallel to learn the codebase: conventions, related code, how to run the project locally (run command, health check, URL, test credentials, side effects that must not fire).
3. Dispatch subagents for outside research (papers, docs, examples, tutorials, etc.) when it helps.
4. Present the goal and 3–8 acceptance criteria. Each criterion states the live check that will prove it.
5. The user confirms once. Goal and criteria are frozen.

## 2. Plan

1. Copy [plan-template](references/plan-template.md) to `docs/plans/<feature>.md` (kebab-case) and fill in every section it asks for, from what you learned above. Leave Architecture and the Slice log empty.
2. Create `feat/<feature>` unless already on a feature branch.

## 3. Architecture

1. Design the high-level shape per [architecture](references/architecture.md): capabilities, which component owns each, the seams between them. Write it into the plan.
2. Dispatch `craft-critic` with the plan.
3. Record each objection in Design rulings as Adopt or Reject, with a reason.
4. Adopted anything? Rewrite the architecture and repeat from 2 with a fresh `craft-critic` subagent. Do not resume the old critic. Otherwise move on.

## 4. Build in slices

Repeat until committed slices cover every acceptance criterion:

1. **Pick** the smallest standalone unit needed next, in dependency order. Wiring finished pieces together counts as a slice.
2. **Design** it with 2–5 observable criteria. Run it past `craft-critic` and record rulings as in step 3. Open a Slice log entry with the frozen criteria.
3. **Build** with `craft-coder`. Brief: the slice, its criteria, the relevant architecture and contracts, conventions and exemplar files.
4. **Check** by running the plan's Verification commands yourself.
5. **Review** with `craft-code-reviewer` over the slice diff. On Revise: resume the coder, then the same reviewer.
6. **Prove** by following [craft-test](../craft-test/SKILL.md) on this slice, using the plan's Live test section to set up (reuse a running environment). If the slice has nothing runnable yet, its tests are the proof; note that in the log.
7. **Commit** with a conventional message once `git diff` contains no `TODO(live-test)` edits. Check the slice off with a Proven line. Update Architecture or Live test if either changed.

If check, review, or proof fails: resume the coder and retry from that step. After 3 resumes, try one fresh coder on Fable. If that fails too, you are stuck.

## 5. Finish

1. `craft-code-reviewer` over the whole branch diff. On Revise: resume the coder, then the same reviewer.
2. `craft-polisher` once, then commit.
3. Run the full Verification list.
4. Follow [craft-test](../craft-test/SKILL.md) against every acceptance criterion, using the live check written for it in step 1. This always runs. Check each criterion off with its evidence.
5. Report criterion by criterion and offer to open a PR.



## When stuck

You are stuck when the slice retry limit is hit, a critic objection cannot be settled or would change a frozen criterion, or the local environment cannot be reached. Write the blocker into the plan, then ask the user. Never guess, never skip.

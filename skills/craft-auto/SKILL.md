---
name: craft-auto
description: Use when the user gives a goal and wants it built autonomously to completion — one interview up front, then architecture, slices, review, and live proof run unattended with the user consulted only when the work cannot converge. Also for resuming a feature that has a docs/plans/ file with a Slice log.
---

# Craft Auto

You are the lead engineer. The user gives you a goal; you interview them once, then build it to completion on your own. Subagents explore, research, critique, implement, review, test, and polish. You decide and you judge; you never write or run feature code yourself.

## Ground rules

- Protect your context. Your job is decisions and gates. Anything else — reading code, searching, researching, running commands, checking a result — goes to a subagent. Use the `craft-*` agents where one fits and a generic subagent (`explore`, `generalPurpose`) for everything else. Do not be afraid to use many subagents in parallel. Read a file yourself only when a decision depends on its exact contents.
- Every subagent gets a full brief; it cannot see this conversation. For corrections, resume the same subagent.
- Pass a model on every dispatch. Newest Fable for critic and the polisher. Newest Grok or Kimi for everything else.
- `docs/plans/<feature>.md` is the single source of truth. Update it as you go.
- Subagent reports are claims. A step is done when the evidence returned shows it working: a command and its output, a response, a screenshot you opened.
- After the user confirms the goal, talk to them only when you are stuck or finished.

**Resuming.** If the plan file already exists, read it and the branch's git log, then pick up where it stopped: empty Slice log means architecture is still open; an unchecked slice or a recorded blocker is the current work.

## 1. Understand

1. Interview the user until you know what to build and what done looks like.
2. Dispatch subagents in parallel to learn the codebase: conventions, related code, how to run the project locally (run command, health check, URL, what the dev environment connects to, the test account, and outbound calls that must not fire).
3. Dispatch `craft-researcher` for outside research (papers, docs, examples, tutorials) when it helps. Several in parallel for independent angles.
4. Present the goal and 3–8 acceptance criteria. Each criterion states the live check that will prove it and, where the flow could reach outside the system, the action the check stops before ("saves the draft; does not Send"). Real data under the test account is expected, not avoided.
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
4. **Review** with `craft-code-reviewer` over the slice diff. On Revise: resume the coder, then the same reviewer.
5. **Test** with `craft-tester`. Brief: the plan's Live test section, the Verification commands, the slice's criteria with their live checks, and the scope. It verifies first, then proves each criterion live and returns a Ran/Saw line per criterion. Judge the evidence per [craft-test](../craft-test/SKILL.md) step 3. If the slice has nothing runnable yet, verification alone is the proof; note that in the log.
6. **Commit** with a conventional message once the tester's cleanup line is clean. Check the slice off with a Proven line. Update Architecture or Live test if either changed.

If review or test fails: resume the coder with the findings and retry from that step. After 3 resumes, try one fresh coder on Fable. If that fails too, you are stuck.

## 5. Finish

1. `craft-code-reviewer` over the whole branch diff. On Revise: resume the coder, then the same reviewer.
2. `craft-polisher` once, then commit.
3. `craft-tester` over the whole feature: the Live test section, the full Verification list, and every acceptance criterion with the live check written for it in step 1. This always runs, even though every slice was tested. Judge the evidence and check each criterion off with it.
4. Push the branch and open a PR with `gh pr create`. Body: what was built, each acceptance criterion with its evidence, and a link to the plan file.
5. Report to the user: the PR link, then each criterion with its evidence.

## When stuck

You are stuck when the slice retry limit is hit, a critic objection cannot be settled or would change a frozen criterion, or the local environment cannot be reached. Write the blocker into the plan, then ask the user. Never guess, never skip.

---
name: craft-refactor
description: Use when the user wants to refactor, clean up, modernize, or simplify existing code.
---

# Craft Refactor

Make existing code simpler, modern, and more idiomatic **without changing what it does**. The user points at a file, package, or feature.

Behavior, public APIs, and wire shapes stay. No new features. Keep the spec in this conversation — do not write it into the target repo.

Prefer, in this order:

1. Does this need to exist?   → no: skip it (YAGNI)
2. Already in this codebase?  → reuse it, don't rewrite
3. Stdlib does it?            → use it
4. Native platform feature?   → use it
5. Installed dependency?      → use it
6. One line?                  → one line
7. Only then: the minimum that works

## 1. Explore

Dispatch subagents to read the target, its callers, tests, and neighbors.

- Form the **boundary**: the narrow interface this code's effects pass through.
- Note what is over-built, unidiomatic, or accidental.
- If there is no narrow boundary, or callers and tests cannot pin the behavior, **steer** in step 6 instead of replacing the code.

If you're unsure whether stdlib, the platform, or an installed dependency already does it, dispatch `craft-researcher`. Adopt only what this project's versions support.

## 2. Spec

Write how the thing should work, not how it currently does. Callers and tests are the source of truth. Keep it in this conversation and put it in every later brief.

- **Purpose** — what callers or users get
- **Behavior** — when X, the system does Y (inputs, outputs, side effects at the boundary)
- **Invariants** — what must always hold
- **Edge cases and errors** — keep the reason, not the mechanism
- **Surface that must stay** — public API, wire shapes, what callers or tests assert
- **Accidents free to die** — internals that are not the contract
- **Non-goals** — no new features

Omit internals unless they *are* the contract. If a behavior is inferred or unknown and would change the design, ask before designing.

## 3. Design

You write the nicer version. Do not dispatch a subagent for this. Design from the spec and the preference list, not by reshuffling the current internals. Look at how this repo does similar things *elsewhere*.

Be concrete: shape, types, what gets deleted. Every element must trace to the spec. Walk the list in order. Do not edit the repo.

## 4. Critic

Dispatch `craft-critic` with the spec, the preference list, and your design — not the old code. Name the files being replaced and forbid reading them.

- **Holds** — move on.
- **Better design** — take it unless you have a concrete reason not to. Rewrite, then dispatch a **fresh** critic. Do not resume the old one. Cap 3 critiques, then stop and ask.

## 5. Compare

Recommend one:

- **Replace** — adopt the new design
- **Keep** — leave the existing code and stop
- **Steer** — refactor the existing code toward the sketch

Tell the user what gets simplified, moved, replaced, or deleted, and why. Wait for their go-ahead.

## 6. Refactor

Dispatch `craft-coder`.

- **Replace:** swap toward the adopted design in small verified waves.
- **Steer:** refactor the existing code toward the sketch.

Then `craft-code-reviewer` over the diff. On Revise: resume the coder, then the same reviewer. Then `craft-polisher`.

Skip any change you cannot tell is behavior-preserving. Do not fix unrelated bugs. Verify it still works.

## 7. Summarize

What changed, what was deleted, and anything you considered but chose not to do.

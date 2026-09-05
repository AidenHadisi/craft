---
name: craft-refactor
description: >-
  Use when the user wants to refactor, clean up, modernize, or simplify
  existing code — making it more idiomatic, readable, and better designed —
  without changing its observable behavior.
---

# Craft Refactor

The user names a file, package, or feature; you diagnose, design, and execute. Observable behavior, public APIs, and wire shapes stay; internals may change freely. You own decisions; subagents explore, research, implement, and review. Every dispatch gets a complete brief; resume the same subagent for corrections.

## 1. Understand

Dispatch parallel exploration subagents to document the target: structure, responsibilities, callers, tests that pin behavior, conventions with exemplar files.

Then form your own diagnosis from the code — not summaries. Where does a reader stall, and why? Unclear, unidiomatic, over-built, badly shaped, or scattered.

## 2. Research

When needed, dispatch web-research for the modern idiomatic way: current language/stdlib APIs, well-maintained packages that could replace hand-rolled code. Verify against this project's versions — never an API the toolchain can't use.

## 3. Design

What changes, moves, merges, collapses, or gets deleted; the key interfaces after; which research you adopt and why. Weigh cognitive load: a first-time reader should follow it in one pass — fewer concepts, definitions near use, one reading order. New dependencies are named here, never mid-wave.

Present briefly with before/after sketches of the key interfaces — one design, no options menu. Proceed on approval.

## 4. Refactor

Small waves, build stays green — leaves first, then callers. Follow every move through callers, imports, and tests.

Per wave: `craft-coder` with the assignment, target contracts, conventions with exemplars, and the files it owns. Run verification, then `craft-code-reviewer` on the wave diff. On revise, resume coder then the same reviewer. Never start the next wave on a red baseline.

## 5. Polish and report

`craft-polisher` over the full diff: footprint, contracts, conventions with exemplars. Run full verification after.

Report: structural change, what was deleted, net line count, anything considered but not done.

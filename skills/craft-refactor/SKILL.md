---
name: craft-refactor
description: >-
  Use when the user wants to refactor, clean up, modernize, or simplify
  existing code — making it more idiomatic, readable, and better designed —
  without changing its observable behavior.
---

# Craft Refactor

Make existing code cleaner, simpler, modern, and more idiomatic without changing what it does. The user points you at a file, package, or feature that may be over-engineered, unidiomatic, dated, or more complex than it needs to be.

## 1. Understand

Read the code and enough of its callers, tests, and neighbors to know how this repo does things. Dispatch subagents to explore what you can't read yourself. Form your own view: where is it over-built, unidiomatic, or hard to follow?

## 2. Research

Dispatch subagents to check outside the repo: current language and stdlib features, well-maintained packages that could replace hand-rolled code, patterns the codebase isn't using yet. Only adopt what works with this project's actual versions.

## 3. Propose

Tell the user what you found and what you'd do: what gets simplified, moved, replaced, or deleted, and why it's better. One recommendation, briefly. Wait for their go-ahead.

## 4. Refactor

Dispatch subagents to implement and review. Observable behavior, public APIs, and wire shapes stay. Skip any change you can't tell is behavior-preserving. Verify it still works.

## 5. Summarize

What changed, what was deleted, and anything you considered but chose not to do.

---
name: craft-design
description: Use when designing or redesigning a UI, page, component, screen, or frontend flow, or when comparing mockup directions before implementing.
---

# Craft Design

Use the host’s native tools for delegation, browsing, terminal work, and user questions. Resolve Craft agent names against available roles, including plugin prefixes, and inherit the configured model unless the user chooses another. Keep read-only roles read-only across all tools. If a required role or tool is unavailable, report the limitation; do not invent capabilities or replace independent review with self-review.

Mock and iterate UI directions until the user picks a winner or hybrid, then implement that design in the product.

Hold the implementation to [architecture](references/architecture.md).

## 1. Understand

Interview to settle details (multiple-choice when possible). Dispatch subagents for repo context: conventions, what exists, how this connects. Keep what they return and put it in later briefs.

## 2. Sketch

If a Canvas skill is installed, follow it to create one interactive canvas. Otherwise, create a local HTML mockup with a variant switcher and open it using the host's browser or preview tools. Show 3–5 structurally different directions, using the repo's visual language. Name each direction and state its core idea, then link or open the mockup for the user.

The user can tweak a variant, combine elements, add a direction, or drop one. Edit the same mockup; preserve unaffected variants. Combining is another mock iteration, not implementation approval. Continue until they explicitly pick a winner or hybrid.

## 3. Implement

Once they approve a design, dispatch `craft-coder` with the chosen direction, the sibling components to mirror, repo conventions, and the architecture standards. Then dispatch `craft-code-reviewer` over the diff. On Revise: resume the coder, then the same reviewer. Preserve existing data flow and behavior.

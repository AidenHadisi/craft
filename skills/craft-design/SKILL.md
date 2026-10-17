---
name: craft-design
description: Use when designing or redesigning a UI, page, component, screen, or frontend flow, or when comparing mockup directions before implementing.
---

# Craft Design

Mock and iterate UI directions until the user picks a winner or hybrid, then implement that design in the product.

Prefer lower-cost models from the latest generation for straightforward exploration, research, and coding from a complete plan. Use stronger models for difficult reasoning. Report any missing capability that blocks the workflow.

Hold the implementation to [architecture](references/architecture.md).

Read project instructions, `.craft/README.md`, and the relevant shared guides before exploring. If the README is missing, dispatch a writable general-purpose subagent with the target repo root, available `craft-init` skill path (or its full instructions), and the initialize-all-guides scope. Wait for it, then read its generated README and relevant guides. If the skill or delegation is unavailable, report the blocker; do not initialize inline. Investigate task-specific gaps and update the shared guides when durable repository facts change. Pass relevant conventions and commands into later briefs.

## 1. Understand

Interview to settle details (multiple-choice when possible). Dispatch subagents for repo context: conventions, what exists, how this connects. Keep what they return and put it in later briefs.

## 2. Sketch

If a Canvas skill is installed, follow it to create one interactive canvas. Otherwise, create a local HTML mockup with a variant switcher and open it using the host's browser or preview tools. Show 3–5 structurally different directions, using the repo's visual language. Name each direction and state its core idea, then link or open the mockup for the user.

The user can tweak a variant, combine elements, add a direction, or drop one. Edit the same mockup; preserve unaffected variants. Combining is another mock iteration, not implementation approval. Continue until they explicitly pick a winner or hybrid.

## 3. Implement

Once they approve a design, dispatch `craft-coder` with the chosen direction, the sibling components to mirror, repo conventions, and the architecture standards. Then dispatch `craft-code-reviewer` over the diff. On Revise: resume the coder, then the same reviewer. Preserve existing data flow and behavior.

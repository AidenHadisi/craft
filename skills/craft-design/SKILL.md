---
name: craft-design
description: Use when designing or redesigning a UI, page, component, screen, or frontend flow, or when comparing mockup directions before implementing.
---

# Craft Design

Focused UI workflow: mock and iterate directions in Canvas until the user picks a winner or hybrid, then implement that design in the product.

### 1. Understanding the task

Understand the task thoroughly before designing or building. Incomplete understanding leads to wrong assumptions and a disappointed user. Never assume on anything important — if unsure, ask.

To build that understanding:

- Interview the user as needed to settle details. Prefer multiple-choice questions unless freeform is required.
- Explore and gather context by dispatching subagent(s).
- From those findings, learn project conventions, what already exists, and how the feature should connect to the current system.

## 2. Sketching

Read and follow the installed Canvas skill before creating or editing any `.canvas.tsx`. Build **one** canvas with a built-in supported variant switcher and 3–5 genuinely different structural directions (not color swaps). Approximate the repo's visual language with Canvas APIs and theme tokens. Name each direction and state its core idea. Link the canvas per the Canvas skill.

The user can tweak a variant, combine elements, add a direction, or drop one. Edit the same canvas and preserve unaffected variants. A request to combine is another mock iteration, not implementation approval. Continue until the user explicitly picks a winner or hybrid.

### 3. Implementing

Once user approved a design, implement the design in the real frontend, preserving existing data flow and behavior.

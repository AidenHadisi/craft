---
name: craft-design
description: Use when designing or redesigning a UI, page, component, screen, or frontend flow, or when comparing mockup directions before implementing.
---

# Craft Design

Focused UI workflow: mock and iterate directions in Canvas until the user picks a winner or hybrid, then implement that design in the product.

```markdown
- [ ] 1. Understand
- [ ] 2. Ground
- [ ] 3. Sketch
- [ ] 4. Iterate
- [ ] 5. Implement UI
```

## Hard rules

1. The user invoked this skill specifically to use Canvas, so use Canvas despite the Canvas skill's normal eligibility exclusions for active development/existing artifacts.
2. Keep variants and iterations in one canvas unless the user asks otherwise.
3. Canvas is a visual-intent mock only: its `cursor/canvas`-only imports and host-theme restrictions do not dictate the shipped UI; implementation uses the repo's real components, tokens, and styles.

## Steps

### 1. Understand

Restate what you're designing or redesigning and what done looks like. Ask at most 1–2 questions only when needed, using `AskQuestion`. Capture audience, job-to-be-done, constraints, must-keep behavior, and desired feel. Skip questions when the conversation already answers them.

### 2. Ground

Dispatch one readonly exploration subagent. When redesigning, find the current implementation. Always pull design system / theme / tokens / type, component library, similar pages, responsive and accessibility conventions. Do not run the full craft workflow or touch product code.

### 3. Sketch

Explicitly read and follow the installed Canvas skill before creating or editing any `.canvas.tsx`. Build **one** canvas with a built-in supported variant switcher and 3–5 genuinely different structural directions (not color swaps). Approximate the repo's visual language with Canvas APIs and theme tokens. Name each direction and state its core idea. Link the canvas per the Canvas skill.

### 4. Iterate

The user can tweak a variant, combine elements, add a direction, or drop one. Edit the same canvas and preserve unaffected variants. A request to combine is another mock iteration, not implementation approval. Continue until the user explicitly picks a winner or hybrid.

### 5. Implement UI

Turn the selection into a concise implementation brief: chosen direction, layout, interactions and states, responsive / accessibility behavior, repo components and tokens to reuse, and exact UI files to touch.

Implement the brief in the real frontend, preserving existing data flow and behavior.

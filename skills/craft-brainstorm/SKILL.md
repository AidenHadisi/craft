---
name: craft-brainstorm
description: >-
  Use when the user wants to brainstorm or discuss a feature idea — exploring
  how it could be built, which tools or packages fit, and what approach makes
  sense — before any plan or implementation exists.
---

# Craft Brainstorm

Think through a feature idea with the user: understand it, do research, then discuss implementation directions and trade-offs together. The deliverable is the conversation itself — never write files, plans, or docs.

### 1. Understanding the idea

Restate the idea in one or two sentences to confirm you got it. Only ask clarifying questions if something genuinely blocks useful research — at most a couple, multiple-choice when possible. If the idea is clear enough, skip questions and go straight to research.

### 2. Quick research

Use subagents to do the research:

- If the idea relates to the current repo, one subagent explores the codebase: what already exists, where this would live, relevant patterns and constraints.
- One or two subagents research the outside world if it seems valuable — for example, looking at papers, tutorials, guides, libraries, packages, tools, how others solve this, or known pitfalls. Use good judgment: often there’s something useful to learn, but if it’s clear that outside research wouldn’t add value for this idea, feel free to skip it.


### 3. Discussing

Come back with 2–4 genuinely different implementation directions. For each: the core idea, what it would use, and honest trade-offs grounded in the research ("the repo already uses X, so this is cheap"). Give your recommendation and why.

Then converse. Answer questions, push on weak spots, dig deeper on a direction if asked (more research if needed). Adapt as the user's picture of the feature sharpens.

### 4. Wrapping up

When the user converges on a direction, give a short chat summary: the chosen approach, key decisions, tools/packages, and open questions. In chat only — no files. If they want to take it further, `/craft-research` or `/craft-plan` pick up from here.

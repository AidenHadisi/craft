---
name: craft-brainstorm
description: >-
  Use when the user wants to brainstorm or discuss a feature idea — exploring
  how it could be built, which tools or packages fit, and what approach makes
  sense — before any plan or implementation exists.
---

# Craft Brainstorm

Think through a feature idea with the user. The deliverable is the conversation — never write files, plans, or docs.

## 1. Understand

Restate the idea in one or two sentences. Ask at most a couple of questions, and only if they block research — multiple-choice when possible. If the idea is clear, skip straight to research.

## 2. Research

Dispatch subagents in parallel:

- Repo: what exists, where this would live, patterns and constraints.
- Outside (0–2): libraries, tools, how others solve this, known pitfalls. Skip if it wouldn't add value.

## 3. Discuss

Present 2–4 genuinely different directions. For each: the core idea, what it uses, honest trade-offs grounded in the research. Recommend one and why.

Then converse: push on weak spots, dig in if asked (more research if needed). Adapt as their picture of the feature sharpens.

## 4. Wrap up

When they converge, a short chat summary: chosen approach, key decisions, tools/packages, open questions. If they want to go further, `/craft-research` or `/craft` pick up from here.

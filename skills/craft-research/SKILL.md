---
name: craft-research
description: >-
  Deep research and planning skill. Use when the user wants to research how to
  build something, plan an approach, learn about a technology, or produce a
  technical document informed by reliable sources.
---

# Craft Research

Help the user research a topic deeply, discuss approaches, and produce a refined markdown document in `Docs/`. This is collaborative — research, discuss, draft, refine together. Dispatch subagents for research; you own the synthesis and the document.

### 1. Understanding the goal

Ask what they want to research or plan. Prefer multiple-choice questions when possible to keep it fast. Clarify scope, constraints, and what the output doc should cover. Never assume on anything important — if unsure, ask.

### 2. Researching

Dispatch multiple subagents to find authoritative information from many angles. Each covers a different angle so you get broad, deep coverage. They should search for official documentation, research papers, whitepapers, technical articles from recognized experts, books, online references, real-world case studies, tutorials, codebases, production examples, known pitfalls, trade-offs, and failure modes. Prioritize reliable, professional sources over random forum posts. Subagents return findings only — you write all files.

### 3. Synthesizing and discussing

Present findings to the user. Discuss trade-offs, approaches, and options together. Answer questions and adapt based on their context and constraints. Don't just dump — have a conversation about what you found and what makes sense for their situation.

### 4. Writing the document

Write a markdown doc to `Docs/<slug>.md` capturing the plan, approach, key decisions, and references. Structure it clearly with inline links to sources. The doc should be useful standalone — someone reading it later should understand the decisions and reasoning without this chat. Keep it practical and actionable, not academic fluff.

Go over the doc with the user. Incorporate feedback, fill gaps, sharpen sections. Iterate until they're satisfied.

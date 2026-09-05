---
name: craft-research
description: >-
  Deep research and planning skill. Use when the user wants to research how to
  build something, plan an approach, learn about a technology, or produce a
  technical document informed by reliable sources.
---

# Craft Research

Research a topic with the user and produce a refined markdown document in `Docs/`. Dispatch subagents for research; you own the synthesis and the document. Subagents return findings only — you write all files.

## 1. Understand

Ask what they want to research or plan. Prefer multiple-choice. Pin scope, constraints, and what the doc should cover.

## 2. Research

Dispatch multiple subagents, each on a different angle. Prefer official docs, papers, expert write-ups, production examples, and known failure modes over random forum posts.

## 3. Discuss

Present findings. Talk through trade-offs and options against their constraints. Adapt before writing.

## 4. Write

Write `Docs/<slug>.md`: the plan, approach, key decisions, and inline source links. Standalone — a later reader should understand the decisions without this chat.

Go over it with the user. Incorporate feedback until they're satisfied.

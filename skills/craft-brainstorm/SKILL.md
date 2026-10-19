---
name: craft-brainstorm
description: >-
  Use when the user wants to think something through: understand a topic,
  explore code or the outside world, and discuss ideas.
---

# Craft Brainstorm

Think something through with the user. The deliverable is the conversation — never write files, plans, or docs.

## 1. Understand

Restate the subject in one or two sentences. Ask a couple of clarifying questions if needed, using multiple choice when possible. If it is already clear, start.

## 2. Explore & Research

Dispatch subagents as needed while you stay in the conversation. Exploration and research may cover:

- Repositories and codebases
- Logs
- Database information
- Outside sources: research papers, tutorials, documentation, and ideas from the web. Use `craft-researcher` subagents as needed.

## 3. Discuss

Discuss the findings with the user. Share ideas and feedback, and address their questions or concerns.

When research reveals distinct approaches that would change the decision, name them and explain the differences that matter. Recommend one when the user asks or the evidence clearly favors it.

Keep the conversation going: challenge weak spots, follow what matters to the user, and dispatch again when a claim needs another look.

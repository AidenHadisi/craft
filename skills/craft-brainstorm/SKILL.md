---
name: craft-brainstorm
description: >-
  Use when the user wants to talk something through: understand it, look into
  the code or the outside world, and discuss.
---

# Craft Brainstorm

Think something through with the user. The deliverable is the conversation — never write files, plans, or docs.

Prefer lower-cost models from the latest generation for straightforward exploration, research, and coding from a complete plan. Use stronger models for difficult reasoning. Report any missing capability that blocks the workflow.

## 1. Understand

Restate the subject in one or two sentences. Ask at most a couple of questions, and only if the answer changes what you look up. Multiple-choice when possible. If it is already clear, start.

## 2. Look it up

Dispatch subagents for the lookup. You stay in the conversation. Only what the discussion needs, in parallel when the questions are independent:

- Repo and code, when the subject lives in this project: read the existing `.craft/README.md` and relevant shared guides, then use a read-only subagent for task-specific gaps: what exists, where, patterns and constraints. Keep discoveries in the conversation; brainstorming does not initialize or update repository guides.
- Outside, when public sources would change the conversation: `craft-researcher` for papers, libraries, docs, how others handle it, known pitfalls.

One pass is enough to start talking. Dispatch again when the conversation asks for another look.

## 3. Discuss

Answer the thing they brought. Lead with what you found and what you make of it.

When the lookup found genuinely different approaches that would change the decision, name them and the difference that matters. Recommend one when they asked for a recommendation or the evidence clearly favors one.

Then converse: push on weak spots, follow what they care about, and dispatch again when a claim needs another look.

## 4. Wrap up

When the conversation settles, a short summary of where it landed: what you understand, any decision, and what is still open.

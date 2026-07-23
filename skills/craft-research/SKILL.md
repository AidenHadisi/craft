---
name: craft-research
description: >-
  Deep research and planning skill. Use when the user wants to research how to
  build something, plan an approach, learn about a technology, or produce a
  technical document informed by reliable sources.
---

# Research

Help the user research a topic deeply, discuss approaches, and produce a refined markdown document in `Docs/`. This is collaborative — research, discuss, draft, refine together.

## Flow

1. **Understand the goal.** Ask what they want to research or plan. Use multiple-choice questions (AskQuestion) when possible to keep it fast. Clarify scope, constraints, and what the output doc should cover.

2. **Research thoroughly.** Dispatch multiple subagents to find authoritative information from many angles. They should search for official documentation, research papers, whitepapers, technical articles from recognized experts, books, online references, real-world case studies, production examples, known pitfalls, trade-offs, and failure modes. Each subagent covers a different angle so you get broad, deep coverage. Prioritize reliable, professional sources over random forum posts.

3. **Synthesize and discuss.** Present findings to the user. Discuss trade-offs, approaches, and options together. Answer questions. Adapt based on their context and constraints. Don't just dump — have a conversation about what you found and what makes sense for their situation.

4. **Draft the document.** Write a markdown doc to `Docs/<slug>.md` capturing the plan, approach, key decisions, and references. Structure it clearly. Include inline links to sources where relevant.

5. **Refine together.** Go over the doc with the user. Incorporate feedback, fill gaps, sharpen sections. Iterate until they're satisfied.

## Ground rules

- Dispatch subagents for research to preserve main agent context.
- Subagents return findings only — the main agent writes all files.
- Always cite sources as inline markdown links.
- Don't fabricate sources or URLs.
- The doc should be useful standalone — someone reading it later should understand the decisions and reasoning without needing this chat.
- Keep the doc practical and actionable, not academic fluff.

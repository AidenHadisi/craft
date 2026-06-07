# Spec template

Use this structure for `docs/specs/<feature>.md`. Describe the idea and requirements — what and why, never how. No code, no file paths, no module names. A product manager and an engineer must both understand it.

```markdown
# <Feature name>

## Summary
One paragraph, plain language. What this is and who it's for.

## Problem
The problem being solved, from the user's perspective.

## Goals
- What success looks like (bullet outcomes).

## Non-goals
- Explicitly out of scope.

## User stories
1. As a <actor>, I want <capability>, so that <benefit>.

## Requirements
### Functional
- Behaviour the feature must exhibit.
### Non-functional
- Performance, security, accessibility, constraints.

## Key scenarios
Walk through the main flows in prose, including edge cases and failure modes.

## Open questions
- Anything still undecided (empty once resolved).
```

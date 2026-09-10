# Design critique

Apply before any design is built. The point is a forced search for a better design, not agreement: every critic must name a rival or show what it compared against, and you must rule on every rival and risk in writing.

## Lenses

One lens per `craft-critic` dispatch; the brief names it.

- **Simplicity** — least design that stays clear; deletion test; every layer, helper, and knob earns its keep today.
- **Idiom & modernity** — how this repo and the current ecosystem would shape it; stdlib and existing dependencies before hand-rolling; a well-maintained package before a bespoke one.
- **Correctness & seams** — failure modes, contracts that leak, dependencies that cycle, state that drifts.

## Models

Pass the model explicitly on every dispatch. Judgment runs on the latest Fable; legwork runs on the latest Grok. Current roster — update here when models change:

| Work | Model |
|---|---|
| `craft-critic`, `craft-code-reviewer`, `craft-polisher` | `claude-fable-5-1-thinking-medium` |
| Exploration, `craft-coder`, live-test legwork | `cursor-grok-4.6-high` |

## Architecture tribunal

Dispatch all three lenses in parallel on the same draft, each with the full brief: goal, requirements, the draft, conventions with exemplar files, rulings so far. Rule on every objection — *Adopt* or *Reject: reason*. An adopted **Major** means rewrite the draft, not patch it, then run one more full round. Cap: 2 rounds; after that decide, and record the disagreements you overruled.

## Slice critique

One critic with the same brief plus the slice design, lens chosen for what this slice risks most, rotating through the lenses over the feature. An adopted Major means redesign the slice and re-run once. Cap: 1 re-run.

## Rulings

Every rival design and every risk raised gets one line in the plan's `## Design rulings`: lens · Adopt/Reject · reason. Rulings are settled — later critics receive them and do not reopen them without new evidence. The lines are how the reasoning survives without keeping critic transcripts in context.

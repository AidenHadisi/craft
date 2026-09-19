# <Feature name>

## Summary

<one or two paragraphs: current state, the gap, what we add, what done looks like>

## Criteria

The definition of done. Frozen after the user confirms. A box is checked only with evidence from a live run.

- [ ] <observable behavior a live test can prove> — proof: <command / request / page and the expected observable; the action to stop before, if any>

## Out of scope

- <exclusion> — <reason when non-obvious>

## Findings

Facts about this repo: paths, current behavior, siblings, conventions, packages present, and things checked and found absent. Later entries win over earlier ones.

- <fact, with the path or command that shows it>

## Architecture

### Components

- **<name>** — <the one job it owns>. Files: `<path>`, `<path>`. Mirrors `<sibling path>` when there is one.

### Seams

- <from> → <to>: <what crosses>

### Key decisions

- <decision> — <why, one line>

## Slices

Each `###` heading is a slice. The first line under it is the slice's goal. The bullets under `**Criteria:**` are its criteria.

### 1. <short title>

<One sentence: what this slice delivers and which component(s) it builds.>

1.1 <One piece of the work: what it does, in which file.>

```ts
<the contract it pins — signature, endpoint, wire shape, error — when a later slice depends on it>
```

1.2 <Next piece, including its edge and error paths.>

**Criteria:**

- <observable behavior a branch review can check in the diff or a tester can run>

**Tests:**

- <one named behavior, one line, asserting one observable outcome>

## Conventions

- <Repo-specific convention implementers must follow — errors, stores, HTTP, tests, frontend layout, etc.> — exemplar: `<path>`

## Verification

- `<build / typecheck / lint command>`
- `<test command>`

## Live test

How to run the project locally and reach the feature: start command, URL, what the dev environment connects to (local or real DB and services), the test account, and outbound calls to stub. Refined as slices land.

## Rulings

Append-only. One line per critic objection.

- <point> · Adopt | Reject · <reason>

## Slice log

Append-only. An entry opens at design time with its criteria and is checked at commit. If stopped, the last entry records the blocker.

- [x] **Slice 1 — <Name>** · `<commit sha>`
  - Criteria: <2–5 observable criteria, frozen at design>
  - Proven: <what was run and what was observed — or why nothing was runnable yet>

# <Feature name>

## What we're building

<One or two paragraphs: current state, the gap, what we're adding, and what done looks like.>

## Requirements

- <Observable requirement>
- <…>

## Out of scope

- <Explicit exclusion — with a brief reason if non-obvious>
- <…>

## Acceptance criteria

<The definition of done. Frozen after the user confirms. A box is checked only with evidence from a live run.>

- [ ] <Observable criterion> — proof: <request / page / command and the expected observable result; the action to stop before, if any>
- [ ] <…>

## Architecture

<The agreed design: components and the one job each owns, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. This section keeps slices converging — keep it current when a slice changes the design.>

## Conventions

- <Repo-specific convention implementers must follow for this feature — errors, stores, HTTP, tests, frontend layout, etc.> — exemplar: `<path>`

## Verification

- `<build / typecheck / lint command>`
- `<test command>`

## Live test

<How to run the project locally and reach the feature: start command, URL, what the dev environment connects to (local or real DB and services), the test account, and outbound calls to stub. Refined as slices land.>

## Design rulings

<Append-only. One line per critic objection.>

- <objection> · Adopt | Reject · <reason>

## Slice log

<Append-only. An entry opens at design time with its criteria and is checked at commit. If stopped, the last entry records the blocker.>

- [x] **Slice 1 — <Name>** · `<commit sha>`
  - Criteria: <2–5 observable criteria, frozen at design>
  - Proven: <what was run and what was observed — or why nothing was runnable yet>
